#!/usr/bin/env python
#-*- coding: utf-8 -*-
#  Copyright 2013 Findspire

'''
File part of Findspire frontend project,
used to handle django custom filters and keywords
'''

import base64
import copy
import datetime
import simplejson, json
import urllib
import re
import math

import dateutil.parser
from django import template
from django.utils import formats
from django.utils.translation import ugettext_lazy

from findspire import settings
from findspire.apps.frontend.utils import LazyEncoder
from findspire.common import music
from findspire.models import Profile, Media, MetadataInterface, ProfileAliasCache, Mode, Genre
from findspire.utils import utils
from findspire.middleware import get_current_request

import findspire.profile
import findspire.models.interfaces

register = template.Library()

VIDEO_QUALITIES = {
    # The first element of the tuple is the filename suffix, the second one is
    # the priority (used for checking which one will be displayed by default).
    "HD": ("-hd", 4),
    "HQ": ("-hq", 3),
    "SD+": ("-mq", 2),
    "SD": ("", 1),
}

@register.filter
def split_list(param, split_by):
    ret = []
    split_size = int(math.ceil(len(param)/float(split_by)))
    for i in range(0, split_by):
        ret += [param[(i*split_size):(i+1)*split_size]]
    return ret

@register.filter
def normalize_boolean(param):
    if param == 'false':
        return False
    if param == 'true':
        return True
    if type(param) is bool and param == True:
        return True
    return False

@register.filter
def get_trailer(profile):
    if not profile:
        return None
    trailers = profile.find_references(tag="trailer", obj_model="media", ready=True, privacy_info=None)
    return len(trailers) and trailers[0] or None


@register.filter
def is_trailer_of(media, profile):
    """ Check if given media is trailer of given profile.
    """
    return media.is_trailer_of(profile)


@register.filter
def is_recommandations(profile_uuid):
    return profile_uuid == settings.RECOMMANDATIONS_UUID and 'true' or 'false'

@register.filter
def is_internal_profile(profile_uuid):
    return profile_uuid in ( settings.RECOMMANDATIONS_UUID, settings.FINDSPIRE_UUID, settings.PUBLICATION_UUID, settings.ILLUSTRATIONS_UUID, settings.BLACKLIST_UUID )

@register.filter
def prepare_playlist(playlist, language):
    request = get_current_request()
    playlist['total_duration'], playlist['alltracks'] = music.get_tracks(
        playlist, request.geo_country_code, owner=False, language=language, active_profile_uuid=None)
    return playlist


@register.filter
def media_label(code):
    return {"image": ugettext_lazy("Images"),
            "video": ugettext_lazy("Videos"),
            "album": ugettext_lazy("Albums")}.get(code, "")

@register.filter
def partial_date_format(date):
    nb_items = len(date.split("-"))
    if nb_items == 1:
        return "Y"
    if nb_items == 2:
        return "F Y"
    return "d F Y"

@register.filter
def format_external_link(link):
    if not link.lower().startswith("http://") and not link.lower().startswith("https://"):
        return 'http://' + link
    return link

@register.filter
def format_iso_date(isodate):
    dtime = dateutil.parser.parse(isodate)
    return formats.date_format(dtime, "DATE_FORMAT")

@register.filter
def mkdate(isodate):
    try:
        dtime = dateutil.parser.parse(isodate)
    except ValueError:
        try:
            dtime = dateutil.parser.parse(isodate.split()[0])
        except ValueError:
            return None
    return dtime

@register.filter
def is_past(isodate):
    try:
        return dateutil.parser.parse(isodate) < datetime.datetime.utcnow()
    except ValueError:
        return None

@register.filter
def format_partial_date(pdate):
    mtch = findspire.models.interfaces.RE_DATE_PARTIAL.match(pdate)
    if not mtch:
        return ''
    year, month, day = mtch.groups()
    ret = str(year)
    if month is not None:
        ret += '-%02d' % int(month)
        if day is not None:
            try:
                datetime.date(int(year), int(month), int(day))
            except ValueError:
                return ''  # Invalid date, such as 2013-02-29
            ret += '-%02d' % int(day)
    return ret

@register.filter
def wrapp_lines(text, size):
    res = []
    for line in text.splitlines():
        newline = ""
        words = line.split(" ")
        for word in words:
            if len(newline + " " + word) > size:
                res += [newline]
                newline = word
            else:
                if newline:
                    newline = newline + " " + word
                else:
                    newline = word
        res += [newline]

    return res


@register.filter
def get_hd_profile_picture(profile):
    return findspire.profile.get_profile_picture(profile, hd=True)

@register.filter
def get_profile_picture(profile, size=None):
    return findspire.profile.get_profile_picture(profile, size=size)

@register.filter
def get_hd_profile_picture_or_default(profile):
    default_pic = settings.STATIC_URL + "frontend/img/profile/default-bkg-full.png"
    return findspire.profile.get_profile_picture(profile, hd=True, default_pic=default_pic)

@register.filter
def get_profile_picture_or_default(profile, size=None):
    if profile['type'] == 'movie':
        default_pic = settings.STATIC_URL + "frontend/img/profile/nobackgroundmovie.png"
    else:
        default_pic = settings.STATIC_URL + "frontend/img/profile/default-bkg-full.png"
    return findspire.profile.get_profile_picture(profile, size=size, default_pic=default_pic)

@register.filter
def get_background_picture(profile, size=None):
    return findspire.profile.get_profile_background_picture_url(profile, size=size)


@register.filter
def get_thumbnail(record, size=None):
    """ Get the record thumbnail.

    :param size: The wanted size ('mini', 'small', 'hd'...)
    """
    if not record:
        return ''
    return record.get_thumbnail(size=size)


@register.filter
def get_legal_lines(media):
    def _fix(lines, prefix):
        for i, l in enumerate(lines):
            for strip_tag in ('(c)', '(p)'):
                if l[:3].lower() == strip_tag:
                    l = l[len(strip_tag):]
            lines[i] = prefix + l.strip()
        return lines

    ret = []
    ret += _fix(media.get_fields_by_type("cline").values(), '(C) ')
    ret += _fix(media.get_fields_by_type("pline").values(), '(P) ')
    return ret

@register.filter
def ensure_absolute_url(url, prefix=None):
    if not url:
        return ""
    if url.startswith("http://") or url.startswith("https://"):
        return url

    if prefix is None:
        prefix = "https://www.findspire.com"
    if url.startswith("//"):
        return "https:" + url
    else:
        return prefix + url

@register.filter
def get_shortdesc(obj):
    if not obj:
        return ""
    if obj['type'] == "movie":
        return obj.get(('metadata', 'basicinfos', 'synopsis'), "")[0:100]
    shortdesc = obj.get(('metadata', 'basicinfos', 'shortdesc'), None)
    if shortdesc:
        return shortdesc
    desc = obj.get(('metadata', 'basicinfos', 'description'), "")
    if len(desc) > 100:
        return desc[0:100] + "..."
    return desc

@register.filter
def endswith(string, end):
    return string.endswith(end)


@register.filter
def sort(tosort):
    tosortcopy = copy.deepcopy(tosort)
    tosortcopy.sort()
    return tosortcopy

@register.filter
def get_modes(obj, language):
    return obj.get_modes(language)

@register.filter
def get_mode_locale(mode_name, language):
    mode = Mode.get(mode_name)
    if not mode:
        return ''
    return mode.get_locale(language)

@register.filter
def get_genre_locale(genre_name, language):
    genre = Genre.get(genre_name)
    if not genre:
        return ''
    return genre.get_locale(language)


@register.filter
def make_range(size, end=None):
    if end is not None:
        start = int(size)
        end = int(end)
        if start > end:
            return range(start, end, -1)
        return range(start, end)
    return range(0, int(size))

@register.filter
def format_object_duration(media, obj_name):
    if ('objects', obj_name, '__metadata__', 'duration') not in media:
        return ""
    ret =  str(datetime.timedelta(seconds=int(media['objects'][obj_name]['__metadata__']['duration'])))
    if ret.startswith("0:"):
        return ret[2:]
    return ret

@register.filter
def format_duration(duration):
    if not duration:
        return "00:00"
    ret = str(datetime.timedelta(seconds=int(duration)))
    if ret.startswith("0:"):
        return ret[2:]
    return ret

@register.filter
def format_duration_minutes(duration):
    if not duration:
        return "0"
    return str(int(duration / 60))

@register.filter
def clear_json(obj):
    return simplejson.dumps(obj, cls=LazyEncoder)

@register.filter
def encoded_json(value):
    """Return a base64-encoded JSON representation of the value"""
    return base64.urlsafe_b64encode(json.dumps(value))

@register.filter
def get_field_type(field_name):
    return MetadataInterface.get_field_type(field_name)

@register.filter
def get_field_config(field_name):
    config = MetadataInterface.get_field_config(field_name)
    if not config:
        return None
    if 'revfield' in config:
        config['inverse'] = MetadataInterface.get_field_config(config['revfield'])
    return config

@register.filter
def get_fields_by_type(obj, field_type):
    if not obj:
        return []
    return obj.get_fields_by_type(field_type)

@register.filter
def encode_keywords_without(keywords, remove):
    keywords = copy.copy(keywords)
    if remove in keywords:
        keywords.remove(remove)
    return "+".join([urllib.quote(keyword) for keyword in keywords])

@register.filter
def encode_keywords_plus(keywords, plus):
    keywords = copy.copy(keywords)
    keywords += [plus]
    return "+".join([urllib.quote(keyword) for keyword in keywords])

@register.filter
def get_profile(profile_uuid):
    return Profile.get(profile_uuid)

@register.filter
def get_media(media_uuid):
    return Media.get(media_uuid)


## FIXME FIXME FIXME: DELETE THIS FUNCTION USED ONLY FOR FELIX THE CAT
@register.filter
def get_album(media_uuid):
    media = Media.get(media_uuid)
    alltracks_uuids = media.get('child_media_uuids', [])

    alltracks = Media.multiget(alltracks_uuids)
    parents = Profile.multiget([media['parent_profile_uuid'] for media in alltracks.values()
                                if media and 'parent_profile_uuid' in media])

    count = 0

    tracks = {}
    for track_uuid in alltracks_uuids:
        track = alltracks.get(track_uuid, None)
        if not track or not track.get('ready', False) or not track.visible:
            continue
        count += 1
        tracks[count] = track
        tracks[count]['track_type'] = "track"
        tracks[count]['owner'] = True
        track.parent_profile = parents.get(track['parent_profile_uuid'], None)

    media['tracks'] = sorted(tracks.items())
    return media

@register.filter
def profile_alias(profile_uuid):
    alias = ProfileAliasCache.get_alias(profile_uuid)
    return alias if alias else profile_uuid


@register.filter
def getindex(record, index):
    ''' getindex filter '''
    try:
        return record[int(index)]
    except:
        return None


@register.filter
def get_video_sources(objects):
    """get_video_sources filter"""

    sources = []
    for vtype in ("mp4", "webm"):
        qualities = {}
        for qual, qual_info in VIDEO_QUALITIES.iteritems():
            suffix, prio = qual_info
            url = utils.get_download_url(objects, "video", vtype + suffix)
            if len(url) > 0:
                qualities[prio] = {
                    "type": "video/"+vtype,
                    "src": url,
                    "res": qual,
                }
        if len(qualities) > 0:
            default_res = qualities[max(qualities.iterkeys())]["res"]
            for quality in qualities.itervalues():
                quality["default"] = "true" if quality["res"] == default_res else "false"
                sources.append(quality)
    return sources

@register.filter
def getitem(obj, key):
    ''' getitem filter '''
    if type(obj) == dict:
        if obj and key:
            return obj.get(key, '')
    elif type(obj) == list:
        if type(key) is str and not key.isdigit():
            return ''
        idx = int(key)
        if idx + 1 > len(obj):
            return ''
        return obj[idx]
    return ''


@register.filter
def get_community_icon_template(community_name):
    return "frontend/svg/community/%s.svg" % community_name

@register.filter
def keys(obj):
    return obj.keys()







class ObjectUrlRenderer(template.Node):
    ''' Renderer for get_object_url keyword '''

    def __init__(self, objects, object_name, object_type, get_default_value=lambda : ""):
        self.objects = objects
        self.object_name = object_name
        self.object_type = object_type
        self.default_value = get_default_value

    def render(self, context):

        object_type = get_value(context, self.object_type)
        object_name = get_value(context, self.object_name)
        objects = get_value_from_context(context, self.objects)
        if not object_type or not object_name or not objects:
            return self.default_value()
        result = utils.get_download_url(objects, object_name, object_type)
        if not result:
            return self.default_value()
        return result


def get_value(context, name):
    if name[0] in ("'", '"'):
        return name[1:-1]
    return get_value_from_context(context, name)

def get_value_from_context(context, name):
    for context_item in name.split("."):

        if type(context) == list:
            if not context or not context_item.isdigit():
                return None
            if len(context) > int(context_item):
                context = context[int(context_item)]
            else:
                return None
        else:
            if not context or context_item not in context:
                if context_item.isdigit():
                    context = context[int(context_item)]
                    continue
                if hasattr(context, context_item):
                    context = getattr(context, context_item)
                    continue
                return None
            context = context[context_item]
    return context


@register.tag(name='get_object_url')
def do_get_object_url(parser, token):
    ''' get_object_url keyword '''

    try:
        keyword_name, objects, object_name, object_type = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r keyword requires three arguments" %
                                           token.contents.split()[0])
    return ObjectUrlRenderer(objects, object_name, object_type)






class DebugModeRenderer(template.Node):
    ''' debug_mode keyword renderer class'''

    def __init__(self):
        pass

    def render(self, context):
        return str(settings.DEBUG).lower()


@register.tag(name='debug_mode')
def do_debug_mode(parser, token):
    ''' debug_mode keyword '''
    return DebugModeRenderer()






def get_custom_tag_param_value(object_type, context):
    ''' get_custom_tag_param_value '''
    if object_type[0] in ("'", '"'):
        return object_type[1:-1]
    else:
        dic = context
        for dic_record in object_type.split("."):
            if dic_record not in dic:
                return None
            dic = dic[dic_record]
        return dic


class RatingStarsRenderer(template.Node):
    ''' get_rating_stars keyword renderer class '''

    def __init__(self, rating, mode):
        self.rating = rating
        self.mode = mode

    def render(self, context):
        rating = get_custom_tag_param_value(self.rating, context)
        mode = get_custom_tag_param_value(self.mode, context)
        if rating is None:
            return ""
        try:
            rating = float(rating)
        except ValueError:
            return ""
        if mode == "on":
            return "*" * int(round((rating / 2.0)))
        else:
            return "*" * int(round(((10.0 - rating) / 2.0)))
        return ""


@register.tag(name='get_rating_stars')
def do_get_rating_stars(parser, token):
    ''' get_rating_stars keyword '''
    try:
        keyword_name, rating, mode = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r keyword requires two arguments" %
                                           token.contents.split()[0])

    return RatingStarsRenderer(rating, mode)





@register.tag(name='captureas')
def do_captureas(parser, token):
    try:
        keyword_name, args = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("'captureas' node requires a variable name.")
    nodelist = parser.parse(('endcaptureas',))
    parser.delete_first_token()
    return CaptureasNode(nodelist, args)

class CaptureasNode(template.Node):
    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        output = self.nodelist.render(context)
        context[self.varname] = output
        return ''

@register.tag
def make_list(parser, token):
    bits = list(token.split_contents())
    if len(bits) >= 4 and bits[-2] == "as":
        varname = bits[-1]
        items = bits[1:-2]
        return MakeListNode(items, varname)
    else:
        raise template.TemplateSyntaxError("%r expected format is 'item [item ...] as varname'" % bits[0])

class MakeListNode(template.Node):
    def __init__(self, items, varname):
        self.items = map(template.Variable, items)
        self.varname = varname

    def render(self, context):
        context[self.varname] = [ i.resolve(context) for i in self.items ]
        return ""


@register.filter
def split(val, arg=None):
    return val.split(arg)

@register.filter
def count(val, arg):
    return val.count(arg)

@register.filter
def multiplicate(val, arg):
    return int(float(val) * float(arg))


NAMESPACE_PROTECTION = False


class define_node(template.Node):
    def __init__(self, value, key, parse):
        self.value = value
        self.key = key
        self.parse = parse

    def render(self, context):
        if NAMESPACE_PROTECTION:
            if self.key in context:
                raise Exception("EPIC NAMESPACE FAIL, CONTEXT HAZ A %s" % self.key)
        if self.parse:
            val = None
            val = context[self.value.split(".")[0]]
            for part in self.value.split(".")[1:]:
                if type(val) is list:
                    if int(part) >= len(val):
                        context[self.key] = ""
                        return ''
                    val = val[int(part)]
                else:
                    try:
                        if part not in val:
                            context[self.key] = ""
                            return ''
                        val = val[part]
                    except:
                        context[self.key] = ""
                        return ''
            context[self.key] = val
        else:
            context[self.key] = self.value
        return ''

@register.tag
def define(parser, token):
    """Definition template tag. Use to define variables in your context within the template.
    Sorta like the {% with "blah" as blah %} tag, but without the {% endwith %} mess.

    Supports two modes:
    Literal mode: argument is encapsulated with quotes (e.g. "blah" or 'blah')
                  variable, is set to the string literal, ex:
                  {% define "fish" as foo %}
    Variable mode: argument is prefixed with a $ (e.g. $blah or $monkey)
                   variable is copied from another context variable, ex:
                   {% define $fish as foo %}

    Namespace protection is also provided if django.conf.settings.DEBUG is True.
    You will get an epic namespace fail if that occurs (please fix it before you deploy)

    TODO:
      * define override nomenclature if you REALLY want to overwrite a variable
        - should decide what nomeclature to use first
      * expand on variables so that {% define $array.blah as foo %} will work
        (this currently WILL NOT)
    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    value, key = m.groups()
    if value[0] == value[-1] and value[0] in ('"', "'"):
        ret = value[1:-1]
        parse = False
    else:
        ret = value
        parse = True
    return define_node(ret, key, parse)
