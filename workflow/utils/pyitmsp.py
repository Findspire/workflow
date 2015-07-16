# -*- coding: utf-8 -*-
# Copyright 2014 Findspire

"""
Library to parse easily metadata from iTunes Music Specification Packages
(ITMSP), in the version 5.0revision1 to 5.2.
"""

import xml.etree.ElementTree as ET

class ITMSP(object):
    """
    Root class, instantiate it with a path to an itmsp package
    """
    NS = '{http://apple.com/itunes/importer}'

    def __init__(self, fd):
        self.data = ET.parse(fd)

        # Ensure it's a supported/tested version
        version = self.data.getroot().get("version")
        if version not in ("music5.0", "music5.1", "music5.2"):
            raise NotImplementedError("ITMSP version not supported: %s" % version)

    def get_language(self):
        """Returns the main language of the package"""
        return self.data.findtext(ITMSP.NS + 'language')

    def get_provider(self):
        """Returns the provider's name"""
        return self.data.findtext(ITMSP.NS + 'provider')

    def get_album(self):
        """Returns an object representing the album"""
        return Album(self.data.find(ITMSP.NS + 'album'), self)

class Metadata(object):
    """Abstract class to parse common metadata"""

    def __init__(self, element, parent=None):
        self.element = element
        self.parent = parent

    def get_vendor_id(self):
        """Returns the vendor_id of the object"""
        return self.element.findtext(ITMSP.NS + 'vendor_id')

    def get_grid(self):
        """Returns the GRID of the object"""
        return self.element.findtext(ITMSP.NS + 'grid')

    def get_title(self):
        """Returns the object's title"""
        return self.element.findtext(ITMSP.NS + 'title')

    def get_title_version(self):
        """Returns the object's title version"""
        title_ver = self.element.findtext(ITMSP.NS + 'title_version')
        if title_ver == "":
            title_ver = None
        return title_ver

    def get_genres(self):
        """Returns the object's genres"""
        genres = []
        for genre in self.element.findall(ITMSP.NS + 'genres/' + ITMSP.NS + 'genre'):
            # First try to use the code (ITMSP 5.1+), then the text (deprecated)
            code = genre.get("code")
            if code is None:
                genres.append(genre.text)
            else:
                genres.append("itunes:" + code)
        return genres

    def get_artists(self):
        """Returns all the main artists of the object"""
        return [Artist(a) for a in self.element.findall(ITMSP.NS + 'artists/' + ITMSP.NS + 'artist')
                if a.findtext(ITMSP.NS + 'primary') == 'true']

    def get_contributors(self):
        """Returns all the contributors of the object, excluding the main
        artists"""
        return [Artist(a) for a in self.element.findall(ITMSP.NS + 'artists/' + ITMSP.NS + 'artist')
                if a.findtext(ITMSP.NS + 'primary') != 'true']

    def get_cline(self):
        """Returns the copyright line of the object"""
        return self.element.findtext(ITMSP.NS + 'copyright_cline')

    def get_pline(self):
        """Returns the product line of the object"""
        return self.element.findtext(ITMSP.NS + 'copyright_pline')

    def get_label(self):
        """Returns the label of the object"""
        return self.element.findtext(ITMSP.NS + 'label_name')

    def get_products(self):
        """Returns the legal informations associated to this object as a list
        of tuples containing the territory (ISO 3166-1 alpha 2 country code),
        in which the rest of the tuple is applicable. Then the price tier,
        the sales start date and a boolean whether the product is cleared for
        sale or not."""
        for p in self.element.findall(ITMSP.NS + 'products/' + ITMSP.NS + 'product'):
            territory = p.findtext(ITMSP.NS + 'territory')
            price_tier = p.findtext(ITMSP.NS + 'wholesale_price_tier')
            start_date = p.findtext(ITMSP.NS + 'sales_start_date')
            cleared_for_sale = p.findtext(ITMSP.NS + 'cleared_for_sale')
            _cleared_for_sale = True
            if cleared_for_sale is not None and cleared_for_sale.lower() == 'false':
                _cleared_for_sale = False
            yield (territory, price_tier, start_date, _cleared_for_sale)

    def get_language(self):
        """Returns the language of the object"""
        lang = self.element.findtext(ITMSP.NS + 'language')
        if lang is None and self.parent is not None:
            lang = self.parent.get_language()
        return lang

    def get_localized_titles(self):
        """Returns the localized version of the track's title as a list of
        tuples, each tuple contains the territory code, and the associated
        title"""
        locales = self.element.findall(ITMSP.NS + 'locales/' + ITMSP.NS + 'locale')
        return [(l.get('name'), l.findtext(ITMSP.NS + 'title'))
                for l in locales]

class Album(Metadata):
    """Class used for parsing an album"""

    def get_upc(self):
        """Returns the UPC of the album"""
        return self.element.findtext(ITMSP.NS + 'upc')

    def get_original_release_date(self):
        """Returns the release date of the album, this date is informative
        only."""
        # datetime YYYY-MM-DD except < 90 days sales
        return self.element.findtext(ITMSP.NS + 'original_release_date')

    def get_artwork_files(self):
        """Returns the list of artwork files shipped with this album. This
        list contains tuples with the file name, the file size, the hash of the
        file as well as the hash method."""
        return [(f.findtext(ITMSP.NS + 'file_name'),
                 int(f.findtext(ITMSP.NS + 'size')),
                 f.findtext(ITMSP.NS + 'checksum'),
                 f.find(ITMSP.NS + 'checksum').get('type'))
                for f in self.element.findall(ITMSP.NS + 'artwork_files/' + ITMSP.NS + 'file')]

    def get_tracks(self):
        """Returns all the tracks of the album"""
        return [Track(t, self) for t in self.element.findall(ITMSP.NS + 'tracks/' + ITMSP.NS + 'track')]

    def get_grouped_tracks(self):
        """Returns all the tracks of the album grouped by volume"""
        volume_count = self.element.findtext(ITMSP.NS + 'volume_count')
        if volume_count is None or int(volume_count) == 1:
            tracks = self.get_tracks()
            return [tracks] if tracks != [] else []
        grouped_tracks = []
        for i in range(1, int(volume_count)):
            grouped_tracks.append([Track(t, self)
                                   for t in self.element.findall(ITMSP.NS + 'tracks/' + ITMSP.NS + 'track')
                                   if t.findtext('volume_number') == str(i)])
        return grouped_tracks

class Artist(object):
    """Class used for parsing an artist"""

    def __init__(self, element):
        self.element = element

    def get_name(self):
        """Returns the name of the artist"""
        return self.element.findtext(ITMSP.NS + 'artist_name')

    def get_apple_id(self):
        """Returns the Apple ID of the artist"""
        return self.element.findtext(ITMSP.NS + 'apple_id')

    def get_roles(self):
        """Returns the list of the roles of the artists in the product in
        which he is included"""
        return [r.text for r in self.element.findall(ITMSP.NS + 'roles/' + ITMSP.NS + 'role')]

    def get_localized_names(self):
        """Returns the localized version of the artist's name"""
        locales = self.element.findall(ITMSP.NS + 'locales/' + ITMSP.NS + 'locale')
        return [(l.get('name'), l.findtext(ITMSP.NS + 'artist_name'))
                for l in locales]

class Track(Metadata):
    """Class used for parsing a track"""

    def get_isrc(self):
        """Returns the ISRC of the track"""
        return self.element.findtext(ITMSP.NS + 'isrc')

    def get_track_number(self):
        """Returns the track number of the track"""
        return int(self.element.findtext(ITMSP.NS + 'track_number'))

    def get_audio_language(self):
        """Returns the track audio language"""
        lang = self.element.findtext(ITMSP.NS + 'audio_language')
        if lang is None and self.parent is not None:
            lang = self.parent.get_language()
        return lang

    def get_parental_advice(self):
        """Returns the parental advice associated to the track, it can be
        explicit, clean or none. It is marked as clean only if it is an edited
        version of an explicit track"""
        return self.element.findtext(ITMSP.NS + 'explicit_content') or "none"

    def get_preview_start_index(self):
        """Returns the start index that should be used for the preview, by
        default, 45s sould be used for tracks longer than 75s else 0s."""
        index = self.element.findtext(ITMSP.NS + 'preview_start_index')
        return float(index) if index is not None else None

    def get_gapless_play(self):
        """Returns a boolean whether a gap separating this track from the
        previous one is included in the audio"""
        gapless = self.element.findtext(ITMSP.NS + 'gapless_play')
        if gapless is not None and len(gapless) > 0:
            return gapless == "true"

    def get_file(self):
        """Returns the informations regarding the file associated with the
        track"""
        f = self.element.find(ITMSP.NS + 'audio_file')
        return (f.findtext(ITMSP.NS + 'file_name'),
                int(f.findtext(ITMSP.NS + 'size')),
                f.findtext(ITMSP.NS + 'checksum'),
                f.find(ITMSP.NS + 'checksum').get('type'))

    def get_pline(self):
        """Returns the track P-Line, defaulting to the album P-Line"""
        pline = super(Track, self).get_pline()
        if pline is None or pline == "":
            pline = self.parent.get_pline()
        return pline
