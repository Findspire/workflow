define(['async', 'backbone', 'jquery', 'underscore', 'jquery.cookie', 'underscore.strings'],
function(async,   Backbone,   $,        _) {
    "use strict";

    var BaseView = Backbone.View.extend({
        last_horiz_scroll_time: 0,
        invert_scroll: true,
        last_scroll: 0,
        dom_cache_activated: true,
        current_url: null,
        navigate_enabled: true,
        left_navigation_button_visible: true,
        base_events: {
            "mousewheel .horiz-scrollable" : "scrollHoriz",
            "mousewheel .vert-scrollable" : "scrollVert",
            "mousewheel .prevent-scroll" : "preventScroll",
            "click .navigate-right": "navigateRightClicked",
            "click .navigate-left": "navigateLeftClicked",
        },
        loading_next_page: false,
        last_page: false,

        /**
         * Should we display an overlay on popup loading?
         *
         * This is for popup only.
         *
         * @see render() method.
         */
        display_overlay_on_loading: false,

        loadTemplates: function(section, template_name, cb) {
            var _this = this;

            $.ajax({
                url: '/ajax/templates/' + window.FS.router.models.site.get('language') + "/" + section + "/" + template_name + "/",
                cache: true,
                async: false,
                success: function(data) {
                    _this.templates = $('<div/>').html(data);
                    cb();
                },
            });
        },

        getTemplate: function(template) {
            return this.templates.find(template).html();
        },

        initialize: function(params) {
            _.bindAll(this, 'sectionRender', 'openPopup', 'closePopup', 'popupKeydown', 'scrollHoriz', 'initScrollBar', 'initScrollBarVert');
            this.xhr = null;
            this.$el.removeClass('scrolled');
            this.$el.find('.scrollbar_container_right').scroll(this.scrollBarVert);
            this.models = params.models;
            if (this.initializeView) {
                this.initializeView(params);
            }
            this.events = $.extend(this.base_events, this.events);

            var _this = this;
            this.models.site.on("disconnect connect clear_cache", function() {
                _this.clearCache();
            });

        },

        showNavigation: function($navigate_div) {
            $navigate_div.show();
        },

        setLeftNavigationButtonVisibility: function($navigate_div, visible) {
            if (visible) {
                $navigate_div.parent().children('.navigate').find('.navigate-left').removeClass('hidden');
            } else {
                $navigate_div.parent().children('.navigate').find('.navigate-left').addClass('hidden');
            }
        },

        setRightNavigationButtonVisibility: function($navigate_div, visible) {
            if (visible) {
                $navigate_div.parent().children('.navigate').find('.navigate-right').removeClass('hidden');
            } else {
                $navigate_div.parent().children('.navigate').find('.navigate-right').addClass('hidden');
            }
        },

        navigateRightClicked: function(event) {
            var $navigate_div = $(event.currentTarget).parent().siblings(".navigate_div");
            this.navigateRight($navigate_div);
            event.preventDefault();
        },

        navigateLeftClicked: function(event) {
            var $navigate_div = $(event.currentTarget).parent().siblings(".navigate_div");
            this.navigateLeft($navigate_div);
            event.preventDefault();
        },

        keydownFunction: function(event) {
            var _this = this;

            if ($(document.activeElement).is("input") ||
                $(document.activeElement).is("textarea")) {
                return true;
            }
            if (this.navigate_enabled) {
                if (event.keyCode === 39) {
                    _.each(this.$el.find(".navigate_div"), function(navigate_div) {
                        _this.navigateRight($(navigate_div));
                    });
                    return true;
                } else if (event.keyCode === 37) {
                    _.each(this.$el.find(".navigate_div"), function(navigate_div) {
                        _this.navigateLeft($(navigate_div));
                    });
                    return true;
                }
            }
            return false;
        },


        scrollToDivClicked: function(event) {
            var div_class = $(event.currentTarget).data().div_class;
            var current_view = this.models.site.get("current_view");
            if (current_view && current_view.navigateLeft) {
                current_view.scrollToDiv("." + div_class);
            }
        },

        clearCache: function() {
            this.last_scroll = 0;
            this.last_scroll_url = null;
            this.current_url = null;
        },

        scrollToDiv: function(selector) {
            if (!this.navigate_enabled) {
                return;
            }
            var divs = this.$el.find(selector);
            var $content = this.$el.find(".navigate_div");
            var _this = this;

            if (divs.length) {
                var $elem = $(divs[0]);
                $content.stop();
                var scroll_to = $content.scrollLeft() + $elem.offset().left - _this.navigate_left_limit - 5;
                $content.animate({
                    scrollLeft: scroll_to
                }, ((scroll_to - $content.scrollLeft()) / 3000 ) * 1000, 'easeOutQuad'); // 3000 pixels per second
            }
        },

        navigateLeft: function($navigate_div) {
            this.navigate($navigate_div, "left");
            return;
        },

        navigateRight: function($navigate_div) {
            this.navigate($navigate_div, "right");
            return;
        },

        navigate: function($navigate_div, direction) {
            var content_width = $navigate_div.width();
            var scroll_to_x = null;
            var _this = this;

            var navigate_left_limit_str, navigate_left_limit;
            if ($navigate_div.data()) {
                navigate_left_limit_str = $navigate_div.data().navigate_left_limit;
                navigate_left_limit = navigate_left_limit_str ? parseInt(navigate_left_limit_str) : 0;
            }

            _.each($navigate_div.find(".anchor"), function(elem) {
                    var $elem = $(elem);
                    var elem_left = $elem.offset().left - $navigate_div.offset().left;
                    var elem_right = elem_left + $elem.width();

                    if (direction == "left") {
                        if ((elem_right > navigate_left_limit && elem_left < navigate_left_limit ) && (scroll_to_x === null || scroll_to_x > elem_right)) {
                            scroll_to_x = elem_right;
                        }
                    } else {
                        if ((elem_right > navigate_left_limit && elem_left > (navigate_left_limit+1) && elem_left < content_width && elem_right > content_width) && (scroll_to_x === null || scroll_to_x > elem_left)) {
                            scroll_to_x = elem_left;
                        }
                    }
            });
            $navigate_div.stop();

            var scroll_to = null;

            if (direction == "left") {
                if (scroll_to_x !== null) { /* Scroll to next anchor element position */
                    scroll_to = $navigate_div.scrollLeft() - content_width + scroll_to_x + 5;
                } else { /* In case there is no eligible anchor, just scroll to next page (add content width to scrollLeft) */
                    scroll_to = $navigate_div.scrollLeft() - content_width;
                }
            } else {
                if (scroll_to_x !== null) { /* Scroll to next anchor element position */
                    scroll_to = $navigate_div.scrollLeft() + scroll_to_x - navigate_left_limit - 5;
                } else { /* In case there is no eligible anchor, just scroll to previous page (substract content width to scrollLeft) */
                    scroll_to = $navigate_div.scrollLeft() + content_width;
                }
            }
            var animationDuration = 800;
            $navigate_div.animate({
                scrollLeft: scroll_to
            }, animationDuration, 'easeOutQuad');
            this.last_scroll = scroll_to;
            this.last_scroll_url = document.location.pathname;
            if (this.last_scroll > 0) {
                this.$el.addClass('scrolled');
            } else {
                this.$el.removeClass('scrolled');
            };
            window.FS.router.views.common.trigger("navigateScroll", $navigate_div[0]);

            setTimeout(function() { _this.hideUselessNavigationButtons($navigate_div); }, animationDuration);
        },

        scrollHoriz: function(event) {
            var $target = $(event.currentTarget);
            event.preventDefault();
            event.stopPropagation();

            if (event.deltaX) {
                // Pointer has X scroll capabilities, do not inverse scroll
                this.invert_scroll = false;
                this.last_horiz_scroll_time = event.timeStamp;
            }

            if (!this.invert_scroll && (event.timeStamp - this.last_horiz_scroll_time) > 1500) {
                this.invert_scroll = true;
            }

            // Firefox fix : deltaFactor is not in pixels but in lines with deltaMode = 1
            if (event.originalEvent.deltaMode != 0)
            {
                // Get line height of the element which is horizontal scrolled
                var lineHeight = parseInt($target['offsetParent' in $.fn ? 'offsetParent' : 'parent']().css('line-height'), 10);
                // Get a deltaFactor in pixels
                event.deltaFactor = lineHeight * Math.abs(event.originalEvent.deltaY);
            };

            if (this.invert_scroll) {
                event.currentTarget.scrollLeft -= event.deltaY * event.deltaFactor;
            } else {
                event.currentTarget.scrollLeft += event.deltaX * event.deltaFactor;
                if (!this.left_navigation_button_visible) {
                    this.hideUselessNavigationButtons($(event.currentTarget).parent(".navigate_div"));
                }
            }

            if ($target.hasClass("navigate_div")) {
                this.last_scroll = event.currentTarget.scrollLeft;
                this.last_scroll_url = document.location.pathname;
                this.showNavigationIfNeeded();

                if (this.last_scroll > 0) {
                    this.$el.addClass('scrolled');
                } else {
                    this.$el.removeClass('scrolled');
                };
            }
            return false;
        },

        preventScroll: function(event){
            event.preventDefault();
            return false;
        },

        scrollVert: function(event) {
            event.preventDefault();

            // Firefox fix : deltaFactor is not in pixels but in lines with deltaMode = 1
            if (event.originalEvent.deltaMode != 0)
            {
                // Get line height of the element which is horizontal scrolled
                var lineHeight = parseInt($(event.currentTarget)['offsetParent' in $.fn ? 'offsetParent' : 'parent']().css('line-height'), 10);
                // Get a deltaFactor in pixels
                event.deltaFactor = lineHeight * Math.abs(event.originalEvent.deltaY);
            };

            event.currentTarget.scrollTop -= event.deltaY * event.deltaFactor;
            return false;
        },

        initScrollBar: function() {
            var $parent = this.$el.find('.scrollbar_content_right').parent();
            if (!$parent.hasClass('scrollbar_container_right')) {
                $parent.addClass('scrollbar_container_right').after('<div class="scrollbar_bg_right"><div class="scrollbar_right"></div></div>');
                this.initScrollBarVert();

                $(window).resize(this.initScrollBarVert);
                this.$el.find('.scrollbar_container_right').scroll(this.scrollBarVert);
            } else {
                this.initScrollBarVert();
            };
        },

        initScrollBarVert: function(event) {
            var _this = this;
            this.$el.find('.scrollbar_container_right').each(function() {
                $(this).removeClass('no_scroll');
                var $scrollbarBg = $(this).next('.scrollbar_bg_right');
                var $scrollbar = $scrollbarBg.find('.scrollbar_right');
                var content = $(this).find('.scrollbar_content_right').get(0);

                var containerHeight = $(this).height();
                var contentHeight = $(content).height();

                if (containerHeight < contentHeight) {
                    $scrollbar.height(Math.round(containerHeight / contentHeight * containerHeight));
                    $scrollbarBg.css('height', $(this).css('height'));
                    $scrollbarBg.css('margin-top', $(this).css('margin-top'));
                    $scrollbarBg.css('margin-bottom', $(this).css('margin-bottom'));

                    if (event != null && event.type == 'resize') {
                        var scrollTop = this.scrollTop;
                        $(this).scrollTop(scrollTop - 1);
                        $(this).scrollTop(scrollTop);
                    };

                    if (!$scrollbar.hasClass('draggable')) {
                        $scrollbar.addClass('draggable').mousedown(_this.scrollBarVertDrag);
                        $scrollbarBg.click(_this.scrollBarVertClicked);
                    };
                }
                else {
                    $(this).addClass('no_scroll');
                };
            });
        },

        scrollBarVert: function(event) {
            var $scrollbar = $(event.currentTarget).next('.scrollbar_bg_right').find('.scrollbar_right');
            var content = $(event.currentTarget).find('.scrollbar_content_right').get(0);

            var containerHeight = $(event.currentTarget).height();
            var progress = event.currentTarget.scrollTop / ($(content).height() - containerHeight);

            var scrollbarTop = progress * (containerHeight - $scrollbar.height());

            $scrollbar.css('top', scrollbarTop + 'px');
        },

        scrollBarVertDrag : function(event) {
            event.preventDefault();

            var $scrollbar = $(event.currentTarget);
            var initialY = event.pageY;
            var initialTop = $('.scrollbar_right').css('top');
            initialTop = parseInt(initialTop.substr(0, initialTop.length - 2), 10);

            $('body').mousemove(function(event) {
                event.preventDefault();

                var $container = $scrollbar.parent().prev('.scrollbar_container_right');
                var content = $container.find('.scrollbar_content_right').get(0);

                var containerHeight = $container.height();
                var scrollbarTop = initialTop - (initialY - event.pageY);
                var scrollbarDims = $scrollbar.get(0).getBoundingClientRect();
                var maxTop = containerHeight - scrollbarDims.height;

                if (scrollbarTop < 0) {
                    scrollbarTop = 0;
                }
                else if (scrollbarTop > maxTop) {
                    scrollbarTop = maxTop;
                };

                var progress = scrollbarTop / maxTop;
                var scrollTop = progress * ($(content).height() - containerHeight);

                $container.scrollTop(scrollTop);
            });

            $('body').mouseup(function(event) {
                $('body').unbind('mousemove');
            });
        },

        scrollBarVertClicked: function(event) {
            if (event.target == this) {
                var $scrollbar = $(this).find('.scrollbar_right');
                var $container = $(this).prev('.scrollbar_container_right');
                var content = $container.find('.scrollbar_content_right').get(0);

                var scrollbarHeight = $scrollbar.height();
                var containerHeight = $container.height();
                var scrollbarTop = event.pageY - this.getBoundingClientRect().top - scrollbarHeight / 2;

                var progress = scrollbarTop / (containerHeight - scrollbarHeight);

                if (progress < 0) {
                    progress = 0;
                } else if (progress > 1) {
                    progress = 1;
                };

                var scrollTop = progress * ($(content).height() - containerHeight);
                $container.animate({ scrollTop: scrollTop }, 300);
            };
        },

        replaceDivs: function(root_div, $el, url, divs, cb) {
            var _this = this;
            if (this.xhr) {
                this.xhr.abort();
                this.xhr = null;
            }
            this.xhr = $.ajax({
                    url: '/ajax/' + root_div + url,
                    cache: false,
                    async: true,
                    success: function(data) {
                        if (typeof(divs) == "string") {
                            $el.find(divs).html(data);
                        } else {
                            var result = $('<div/>').html(data);
                            _.each(divs, function(div) {
                                $el.find(div).html(result.find(div).html());
                            });
                        }
                        _this.initScrollBar();
                        if (cb) {
                            cb();
                        }
                    }
            });
        },

        updatePageTitle: function() {
            var $page_infos = this.$el.find(".page_infos");
            if ($page_infos.length) {
                var page_infos = $page_infos.data();
                document.title = page_infos.title;
            }
        },

        updateContent: function(data, $el) {
            if ($.cookie().active_profile_uuid !== this.models.site.get('profile_uuid')) {
                this.models.site.set('profile_uuid', $.cookie().active_profile_uuid, {silent: true});
                this.models.site.trigger('change:profile_uuid', $.cookie().active_profile_uuid);
            }

            $el.html(data);
            if (this.$popup) {
                $el.removeAttr("class");
                $el.addClass(this.section);
            }

            this.updatePageTitle();
            this.delegateEvents();
        },

        showNavigationIfNeeded: function() {
            var _this = this;
            _.each(this.$el.find(".navigate_div"), function(navigate_div) {
                var $navigate_div = $(navigate_div);
                _this.showNavigation($navigate_div);
                _this.hideUselessNavigationButtons($navigate_div);
            });
        },

        hideUselessNavigationButtons: function($navigate_div) {
            if ($navigate_div.length) {
                var navigate_left_limit = parseInt($navigate_div.data('navigate_left_limit'), 10);
                if (isNaN(navigate_left_limit)) {
                    navigate_left_limit = 0;
                }
                if ($navigate_div.scrollLeft() === 0) {
                    this.left_navigation_button_visible = false;
                    this.setLeftNavigationButtonVisibility($navigate_div, false);
                } else {
                    this.left_navigation_button_visible = true;
                    this.setLeftNavigationButtonVisibility($navigate_div, true);
                }
                if ($navigate_div[0].scrollWidth == $navigate_div.scrollLeft() + $navigate_div.width() + navigate_left_limit) {
                    this.setRightNavigationButtonVisibility($navigate_div, false);
                } else {
                    this.setRightNavigationButtonVisibility($navigate_div, true);
                }
            }
        },

        loadAjax: function(options, targetDiv, hideContent, cb) {
            var _this = this,
                url = this.$popup ? window.FS.router.popupUrl : window.location.pathname,
                data = {},
                $el;

            if (this.$popup) {
                $el = this.$popup;
            } else {
                if (targetDiv === 'all') {
                    $el = this.$el;
                } else {
                    $el = this.$el.find("." + targetDiv);
                }
            }

            if (window.location.search[0] == '?') {
                data = _.toQueryParams(window.location.search.substr(1));
            }

            if (!this.$popup) {
                if ( this.dom_cache_activated && url == this.current_url && this.invalidationCheck && this.invalidationCheck(options)) {
                    this.current_url = null;
                    this.last_scroll_url = null;
                }
                if ( this.dom_cache_activated && url == this.current_url) {
                    $('div[id^="section_"]:not(#section_' + this.section + ')').addClass('hidden');
                    this.$el.removeClass("hidden");
                    this.updatePageTitle();
                    this.delegateEvents();

                    if (cb)
                        cb();
                    return;
                }

                $('div[id^="section_"]:not(#section_' + this.section + ')').addClass('hidden');
            }

            if (this.xhr) {
                this.xhr.abort();
                this.xhr = null;
            }
            this.xhr = $.ajax({
                url: '/ajax/' + targetDiv + url,
                cache: false,
                async: true,
                data: data,
                success: function(data) {
                    _this.updateContent(data, $el);
                    _this.current_url = url;
                    if (cb)
                        cb();
                },
                error: function(jqXHR, textStatus, error) {
                    console.log("Ajax error:", jqXHR.status, error);
                    if (cb)
                        cb(error);
                }
            });
        },

        render: function(options, force) {
            var _this = this,
                args = arguments,
                targetDiv;

            this.options = options;

            if (this.$popup) {
                targetDiv = 'popup';
                if (this.display_overlay_on_loading === true) {
                    // Display overlay to highlight the fact viewer is loading. Refs #281
                    this.$popup.parent().css('visibility', 'visible');
                    this.$popup.addClass('overlay').addClass('loading').css('visibility', 'visible');
                }
            }
            else if (arguments.length > 1)
                targetDiv = args[1];
            else if (!this.$el.hasClass("hidden"))
                targetDiv = 'content';
            else
                targetDiv = 'all';

            if (this.current_url && this.current_url == window.location.pathname) {
                if (this.sectionActivated) {
                    this.$el.css("visibility", "hidden");
                    this.$el.removeClass("hidden");
                    $('div[id^="section_"]:not(#section_' + _this.section + ')').addClass('hidden');
                    _this.$el.css("visibility", "visible");
                    this.sectionActivated(function() {
                        _this.delegateEvents();
                        _this.$el.css("visibility", "visible");
                    });
                } else {
                    this.models.site.trigger("windowresized");
                    this.$el.removeClass("hidden");
                    $('div[id^="section_"]:not(#section_' + this.section + ')').addClass('hidden');
                }
                return this;
            }

            this.delegateEvents();
            async.series([
                function(cb) {
                    if (_this.models.site.first_load && force !== true) {
                        _this.models.site.first_load = false;
                        _this.current_url = window.location.pathname;
                        targetDiv = "root_wrapper";
                        $(".root_wrapper").removeClass("loading");
                        cb();
                    }
                    else {
                        if (targetDiv == 'all') {
                            _this.$el.addClass("loading");
                        } else {
                            _this.$el.find("." + targetDiv).addClass("loading");
                        }
                        _this.$el.removeClass("hidden");
                        _this.loadAjax(options, targetDiv, !_this.$popup, cb);
                    }
                },
                function(cb) {
                    // Call _this.sectionRender(cb, *args). Yeah. JS.
                    var cb_args = _.flatten([cb, args]);
                    if (!_this.$popup) {
                        _this.$el.find("." + targetDiv).addClass("loading");
                        if (targetDiv == 'all') {
                            _this.$el.removeClass("loading");
                        } else {
                            _this.$el.find("." + targetDiv).removeClass("loading");
                        }
                    }
                    _this.sectionRender.apply(_this, cb_args);
                },
                function(cb) {
                    // FIXME: this is a workaround. When browsing from /fr/find/
                    // to /fr/inspirations, the background image is not removed,
                    // because it wasn't set in the model, so no event is
                    // triggered when sectionRender() sets it to null. This
                    // should be removed as soon as everything is backbonified.

                    _this.initScrollBar();

                    _this.showNavigationIfNeeded();

                    if (targetDiv == 'all') {
                        $(".all").removeClass("loading");
                    } else {
                        _this.$el.find("." + targetDiv).removeClass("loading");
                    }
                    $(".root_wrapper").css('visibility', 'visible');


                    if (!_this.$popup) {

                        _this.$el.find("." + targetDiv).removeClass("loading");

                        if (_this.dom_cache_activated && _this.current_url == _this.last_scroll_url) {
                            _this.$el.find(".navigate_div").scrollLeft(_this.last_scroll);
                        } else {
                            _this.last_scroll = 0;
                        }
                    }
                    else {
                        $("#popup").css('visibility', 'visible');

                        $(window).on("keydown", _this.popupKeydown);
                    }

                    _this.$el.find('[autofocus]').focus();

                    cb();
                },
            ]);

            return this;
        },

        openPopup: function(options) {
            this.$popup = $("#popupWrapper");
            this.$popup.show();
            this.render(options, true);
        },

        closePopup: function() {
            // Unbind popup-specific events
            if (!this.$popup) {
                return ;
            }

            // Abord previous ajax calls before close the popup
            if (this.xhr) {
                this.xhr.abort();
                this.xhr = null;
            }

            $(window).off("keydown", this.popupKeydown);

            if (this.undelegate)
                this.undelegate();
            this.undelegateEvents();
            this.models.site.set("current_popup_view", null);

            this.showNavigationIfNeeded();

            $("#popup").css('visibility', '');
            this.$popup.empty();
            this.$popup = null;
            window.FS.router.popupUrl = null;
        },

        popupKeydown: function(event) {
            if (this.keydown) {
                this.keydown(event.keyCode);
            }
        },

    });

    return BaseView;
});
