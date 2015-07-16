#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2014 Findspire


""" Here is written the navigation configuration.

Would be nice to have explanations about available configuration items, organization of the
configuration object and where it is used.


# Category configuration
## Items available in search dict
sort: Can be either:
    - The name of an attribute to sort the results on;
    - A dictionary containing the following entries:
        - 'field': The name of an attribute to sort the results on (mandatory);
        - 'apply_on_selection': A boolean telling whether to use the sort on selections (optional).

"""
SELECTION_LOCALES = { "fr": "FINDSPIRE Selection", "en": "FINDSPIRE Selection" }

navigation = [ {
        "code": "visualarts",
        "locales": { "fr": "Arts visuels", "en": "Visual arts"},
        "welcome": {
            "boxes": [ {
                    "locale": { "fr": "Focus sur", "en": "Focus on" },
                    "boxtype": "fullsize",
                    "records": {
                        "main": { "type": ["video"], "category": "photography", "recommandations": "hidden-profile", "nb_items": 1 }
                    },
                 }, {
                    "locale": { "fr": "Photographie", "en": "Photography" },
                    "params": {
                        "link": { "fr": "Notre sélection", "en": "Our selection" },
                        "target": "visualarts/photography/selection/",
                    },
                    "boxtype": "recobox",
                    "records": {
                        "main":   { "type": ["image"], "category": "photography", "recommandations": "selection-top", "nb_items": 1 },
                        "bottom": { "type": ["image"], "category": "photography", "recommandations": "selection-bottom", "nb_items": 2 }
                    },
                }, {
                    "locale": { "fr": "Creative Content", "en": "Creative Content" },
                    "boxtype": "fullsize",
                    "params": {
                        "link": { "fr": "Notre sélection de vidéos", "en": "Our selection of videos" },
                        "target": "visualarts/creativecontent/selection/",
                    },
                    "records": {
                        "main": { "type": ["video"], "category": "creativecontent", "recommandations": "selection-top", "nb_items": 1 }
                    },
                }, {
                    "locale": { "fr": "Illustration / Design Graphique", "en": "Illustration / Graphic Design" },
                    "params": {
                        "link": { "fr": "Notre sélection", "en": "Our selection" },
                        "target": "visualarts/illustrationgraphicdesign/selection/",
                    },
                    "boxtype": "recobox",
                    "records": {
                        "main":   { "type": ["image"], "category": "illustrationgraphicdesign", "recommandations": "selection-top",    "nb_items": 1 },
                        "bottom": { "type": ["image"], "category": "illustrationgraphicdesign", "recommandations": "selection-bottom", "nb_items": 2 }
                    },
                }, {
                    "locale": { "fr": "3D & Animation", "en": "3D & Animation" },
                    "params": {
                        "link": { "fr": "Notre sélection de vidéos d'animation 3D", "en": "Our selection of 3D Animation" },
                        "target": "visualarts/3danimation/animation3d/",
                    },
                    "boxtype": "fullsize",
                    "records": {
                        "main": { "type": ["video"], "category": "3danimation", "recommandations": "selection-top", "nb_items": 1 }
                    },
                }, {
                    "locale": { "fr": "Art urbain", "en": "Urban Art" },
                    "params": {
                        "link": { "fr": "Notre sélection", "en": "Our selection" },
                        "target": "visualarts/urbanart/selection/",
                    },
                    "boxtype": "recobox",
                    "records": {
                        "main":   { "type": ["image"], "category": "urbanart", "recommandations": "selection-top",    "nb_items": 1 },
                        "bottom": { "type": ["image"], "category": "urbanart", "recommandations": "selection-bottom", "nb_items": 2 }
                    },
                }, {
                    "locale": { "fr": "Inspirez vous", "en": "Get inspired"},
                    "params": {
                        "portraits": {
                            "link": { "fr": "Reportage Photo", "en": "Photo Reportage" },
                            "template": "image",
                            "target": "visualarts/photography/reportage/",
                        },
                        "ads": {
                            "link": { "fr": "Arts Publicitaires", "en": "Advertising Arts" },
                            "template": "video",
                            "target": "visualarts/advertisingarts/selection/",
                        },
                        "animation": {
                            "link": { "fr": "L'animation 2D", "en": "2D Animation" },
                            "template": "video",
                            "target": "visualarts/3danimation/animation2d/",
                        },
                        "videos": {
                            "link": { "fr": "Le Dessin à la Main", "en": "Handmade Drawing" },
                            "template": "video",
                            "target": "visualarts/illustrationgraphicdesign/handdrawing/",
                        },
                    },
                    "boxtype": "discoveralso",
                    "records": {
                        "portraits": { "type": ["image"], "category": "photography",     "recommandations": "seealso-photography",     "nb_items": 2 },
                        "ads":       { "type": ["video"], "category": "advertisingarts", "recommandations": "seealso-advertisingarts", "nb_items": 2 },
                        "animation": { "type": ["video"], "category": "3danimation",     "recommandations": "seealso-3danimation",     "nb_items": 2 },
                        "videos":    { "type": ["video"], "category": "creativecontent", "recommandations": "seealso-creativecontent", "nb_items": 2 },
                    }
                }
            ],
        },
        "categories": [ {
                "code": "photography", #OK
                "default_genre": "selection",
                "with_selection": True,
                "genres_family": "imagephotography",
                "minimum_results": 0,
                "search": { "community": "visualarts", "record_type": "image", "mode": "photography" },
                "locales": { "fr": "Photographie", "en": "Photography" }
            }, {
                "code": "illustrationgraphicdesign", #OK
                "default_genre": "selection",
                "with_selection": True,
                "minimum_results": 0,
                "genres_family": "imageillustrationgraphicdesign",
                "search": { "community": "visualarts", "record_type": "image", "mode": "illustrationgraphicdesign" },
                "locales": { "fr": "Illustration / Design graphique", "en": "Illustration / Graphic design" }
            }, { 
                "code": "3danimation",  
                "default_genre": "selection",
                "minimum_results": 0,
                "with_selection": True,
                "selection_conf": {
                        "record_type": ['video', 'image'],
                        "alternate": {"image": 6, "video": 2},
                        "search": {},#FIXME
                    },
                "alternate": {"image": 6, "video": 2},
                "prepend": [{
                        "code": "animation2d",
                        "locales": { "fr": "Animation 2D", "en" : "2D Animation"},
                        "search": { "community": "visualarts", "record_type": "video", "mode": "animation" },
                        "genres_family": "videoanimation",
                    }, { 
                        "code": "animation3d",
                        "locales": { "fr": "Animation 3D", "en" : "3D Animation"},
                        "search": { "community": "visualarts", "record_type": "video", "mode": "animation" },
                        "genres_family": "videoanimation",
                    } ],
                "genres_family": "image3d",
                "search": { "community": "visualarts", "record_type": "image", "mode": "3d" },
                "locales": { "fr": "3D & Animation", "en": "3D & Animation" }
            }, {
                "code": "urbanart",  
                "selection_conf": {
                        "record_type": ['video', 'image'],
                        "alternate": {"image": 6, "video": 2},
                        "search": {},#FIXME
                    },
                "default_genre": "selection",
                "with_selection": True,
                "minimum_results": 20,
                "genres_family": "urbanart",
                "search": { "community": "visualarts", "obj_model": "media", "mode": "urbanart" },
                "alternate": {"image": 6, "video": 2},
                "locales": { "fr": "Art urbain", "en": "Urban Art" }
            }, {

                "code": "advertisingarts",
                "default_genre": "selection",
                "with_selection": True,
                "minimum_results": 20,
                "genres_family": "advertisingarts",
                "search": { "community": "visualarts", "record_type": "image", "mode": "advertisingarts" },
                "locales": { "fr": "Arts publicitaires", "en": "Advertising Arts" }
            }, {
                "code": "creativecontent",
                "default_genre": "selection",
                "with_selection": True,
                "minimum_results": 10,
                "genres_family": "creativecontent",
                "search": { "community": "visualarts", "record_type": "video", "mode": "creativecontent" },
                "locales": { "fr": "Creative Content", "en": "Creative content" }
            }],
    }, {
        "code": "music",
        "locales": { "fr": "Musique", "en": "Music"},
        "welcome": {
            "boxes": [ {
                    "locale": { "fr": "Focus sur", "en": "Focus on" },
                    "boxtype": "fullsize",
                    "records": {
                        "main": { "type": ["video"], "category": "musicvideo", "recommandations": "hidden-profile", "nb_items": 1 }
                    }
                }, {
                    "locale": { "fr": "Nouveautés", "en": "New releases" },
                    "boxtype": "soundtracks",
                    "records": {
                        "main":   { "type": ["album"], "category": "bestalbums", "recommandations": "hidden-news-top",    "nb_items": 1 },
                        "bottom": { "type": ["album"], "category": "bestalbums", "recommandations": "hidden-news-bottom", "nb_items": 4 }
                    }
                }, {
                    "locale": { "fr": "Playlists recommandées", "en": "Recommended Playlists" },
                    "params": {
                        "link": { "fr": "Découvrez toutes les playlists", "en": "Discover all playlists" },
                        "target": "music/playlists/selection/",
                    },
                    "boxtype": "recobox",
                    "records": {
                        "main":   { "type": ["playlist"], "category": "playlists", "recommandations": "hidden-playlists-top",    "nb_items": 1 },
                        "bottom": { "type": ["playlist"], "category": "playlists", "recommandations": "hidden-playlists-bottom", "nb_items": 2 }
                    }
                }, {
                    "locale": { "fr": "Vidéos recommandées", "en": "Recommended Videos" },
                    "params": {
                        "link": { "fr": "Accédez à toutes les vidéos", "en": "All videos" },
                        "target": "music/musicvideo/selection/",
                    },
                    "boxtype": "fullsize",
                    "records": {
                        "main":   { "type": ["video"], "category": "musicvideo", "recommandations": "selection-top", "nb_items": 2 }
                    }
                }, {
                    "locale": { "fr": "Albums recommandés", "en": "Recommended Albums" },
                    "params": {
                        "link": { "fr": "Ecoutez des millions de titres", "en": "Discover millions of tracks" },
                        "target": "music/universe/selection/",
                    },
                    "boxtype": "soundtracks",
                    "records": {
                        "main":   { "type": ["album"], "category": "universe", "recommandations": "selection-top",    "nb_items": 1 },
                        "bottom": { "type": ["album"], "category": "universe", "recommandations": "selection-bottom", "nb_items": 4 }
                    }

                }, {
                    "locale": { "fr": "Découvrez aussi dans FINDSPIRE MUSIQUE", "en": "Discover also on FINDSPIRE MUSIC"},
                    "params": {
                        "bestalbums": {
                            "link": { "fr": "Top Albums par années", "en": "Best albums by year" },
                            "template": "album",
                            "target": "music/bestalbums/2010s/",
                        },
                        "musicvideo": {
                            "link": { "fr": "Meilleurs clips vidéos", "en": "Best music videos" },
                            "template": "video",
                            "target": "music/musicvideo/selection/",
                        },
                        "besttracks": {
                            "link": { "fr": "Top Titres par année", "en": "Best tracks by year" },
                            "template": "album",
                            "target": "music/besttracks/2014/",
                        },
                        "playlists": {
                            "link": { "fr": "Playlists Thématiques", "en": "FINDSPIRE Playlists" },
                            "template": "playlist",
                            "target": "music/playlists/themes/",
                        },
                    },
                    "boxtype": "discoveralso",
                    "records": {
                        "bestalbums": { "type": ["album"],    "category": "universe",   "recommandations": "seealso-bestalbums", "nb_items": 3 },
                        "musicvideo": { "type": ["video"],    "category": "musicvideo", "recommandations": "seealso-musicvideo", "nb_items": 2 },
                        "besttracks": { "type": ["album"],    "category": "besttracks", "recommandations": "seealso-besttracks", "nb_items": 3 },
                        "playlists":  { "type": ["playlist"], "category": "playlists",  "recommandations": "seealso-playlists",  "nb_items": 2 },
                    }
                }]
        },
                

        "categories": [ {
                "code": "universe",
                "default_genre": "selection",
                "with_selection": True,
                "geo_restrictions": True,
                "genres_family": "music",
                "search": {
                    "record_type": "album",
                    "community": "music",
                    "mode": ["album", "epsingle"],
                    "sort": ["metadata.basicinfos.release_date"],
                    },
                "locales": { "fr": "Univers", "en": "Universe" }
            }, {
                "code": "musicvideo",
                "default_genre": "selection",
                "with_selection": True,
                "genres_family": "music",
                "minimum_results": 0,
                "search": {"record_type": "video", "mode": "musicvideo", "community": "music"},
                "locales": { "fr": "Clips vidéo", "en": "Music video" }
            }, {
                "code": "playlists",
                "default_genre": "selection",
                "with_selection": True,
                "recommandations": True,
                "minimum_results": 0,
                "genres_family": "musicplaylists",
                "search": {"record_type": "playlist"},
                "locales": { "fr": "Playlists", "en": "Playlists" }
            }, {
                "code": "bestalbums",
                "default_genre": "2010",
                "geo_restrictions": True,
                "recommandations": True,
                "minimum_results": 0,
                "genres_family": "bestalbums",
                "search": { "community": "music", "record_type": "album"},
                "locales": { "fr": "Meilleurs albums", "en": "Best albums" }
            }, {
                "code": "besttracks",
                "default_genre": "2010",
                "geo_restrictions": True,
                "recommandations": True,
                "display": "tracks",
                "minimum_results": 0,
                "genres_family": "besttracks",
                "search": { "community": "music", "record_type": "playlist"},
                "locales": { "fr": "Meilleurs titres", "en": "Best tracks" }
            }, {
                "code": "allplaylists",
                "default_genre": "all",
                "genres_family": "musicplaylists",
                "search": {"obj_model": "playlist", "record_type": "playlist"},
                "locales": { "fr": "All playlists", "en": "Toutes les playlists" },
                "staff_only": True,
                "ignore": True,
            }, {
                "code": "all",
                "default_genre": "all",
                "staff_only": True,
                "genres_family": "music",
                "search": { "community": "music", "record_type": "album", "sort": ["publication.publication_date"], "publication": "published", "record_type": "album"},
                "locales": { "fr": "Tous les albums", "en": "All albums" },
                "ignore": True,
            } ]
    } , {
        "code": "cinema",
        "maxrecords_anonymous": 20,
        "locales": { "fr": "Cinéma", "en": "Cinema" },
        "welcome": {
            "boxes": [ {
                    "locale": { "fr": "Focus sur", "en": "Focus on" },
                    "boxtype": "moviefullsize",
                    "records": {
                        "main": { "type": ["video"], "category": "movies", "recommandations": "hidden-profile", "nb_items": 1 }
                    }
                }, {
                    "locale": { "fr": "Les films à l'affiche", "en": "Performing movies" },
                    "params": {
                        "link": { "fr": "Découvrez tous les films à l'affiche", "en": "iscover all performing movies" },
                        "target": "cinema/movies/performing/",
                    },
                    "boxtype": "boxes",
                    "records": {
                        "main": { "type": ["movie"], "category": "movies", "recommandations": "hidden-performing", "nb_items": 4 }
                    }
                }, {
                    "locale": { "fr": "Les Courts", "en": "Short films" },
                    "params": {
                        "link_disabled": { "fr": "Découvrez tous les courts métrages", "en": "Découvrez tous les courts métrages" },
                        "target": "cinema/shorts/selection/",
                    },
                    "boxtype": "fullsize",
                    "records": {
                        "main": { "type": ["video"], "category": "shorts", "recommandations": "selection-top", "nb_items": 1 }
                    }
                }, {
                    "locale": { "fr": "Les Bandes originales", "en": "Original Soundtracks" },
                    "params": {
                        "link": { "fr": "Découvrez les plus grandes musiques de films", "en": "Découvrir the greatest soundtracks" },
                        "target": "cinema/soundtracks/selection/",
                    },
                    "boxtype": "soundtracks",
                    "records": {
                        "main":  { "type": ["album"], "category": "soundtracks", "recommandations": "2010s-top",    "nb_items": 1 },
                        "bottom": { "type": ["album"], "category": "soundtracks", "recommandations": "2010s-bottom", "nb_items": 4 }
                    }
                }, {
                    "locale": { "fr": "Découvrez aussi dans FINDSPIRE Cinéma", "en": "Discover also on FINDSPIRE Cinema" },
                    "params": {
                        "soundtracks": {
                            "link": { "fr": "Tout l'univers du cinéma en musique", "en": "Tout l'univers du cinéma en musique" },
                            "template": "album",
                            "target": "cinema/soundtracks/selection/",
                        },
                        "shorts": {
                            "link": { "fr": "Une sélection de courts métrages exclusifs", "en": "Une sélection de courts métrages exclusifs" },
                            "template": "video",
                            "target": "cinema/soundtracks/selection/",
                        },
                        "bestmovies": {
                            "link": { "fr": "Top Films par année", "en": "Top Films par année" },
                            "template": "movie",
                            "target": "cinema/bestmovies/byyear-2014/",
                        },
                        "mostwanted": {
                            "link": { "fr": "Les prochaines sorties", "en": "Les prochaines sorties" },
                            "template": "movie",
                            "target": "cinema/movies/upcoming/",
                        },
                    },
                    "boxtype": "discoveralso",
                    "records": {
                        "soundtracks": { "type": ["album"], "category": "soundtracks", "recommandations": "seealso-soundtracks", "nb_items": 3 },
                        "shorts":      { "type": ["video"], "category": "shorts",      "recommandations": "seealso-shorts",      "nb_items": 2 },
                        "bestmovies":  { "type": ["movie"], "category": "bestmovies",  "recommandations": "seealso-bestmovies",  "nb_items": 3 },
                        "mostwanted":  { "type": ["movie"], "category": "movies",      "recommandations": "seealso-mostwanted",  "nb_items": 3 },
                    }
                }
            ],
        },

        "categories": [ {
                "code": "movies",
                "with_selection": True,
                "default_genre": "selection",
                "search": { "community": "cinema", "record_type": "movie" },
                "locales": { "fr": "Longs métrages", "en": "Feature films" },
                "selection_conf": {
                    "search": { "record_type": ['video'] }
                },
                "prepend": [{
                        "code": "thisweek",
                        "genres_family": "movies",
                        "locales": { "fr": "Sorties de la semaine", "en" : "New this week"},
                        "search": { "community": "cinema", "record_type": "movie", "filter": "news"},
                    }, {
                        "code": "performing",
                        "genres_family": "movies",
                        "locales": { "fr": "En salle", "en" : "Performing"},
                        "search": { "community": "cinema", "record_type": "movie", "filter": "performing"},
                    }, {
                        "code": "nextweek",
                        "genres_family": "movies",
                        "locales": { "fr": "Mercredi prochain", "en" : "Upcoming"},
                        "search": { "community": "cinema", "record_type": "movie", "filter": "news+1"},
                    }, {
                        "code": "later",
                        "genres_family": "movies",
                        "locales": { "fr": "Prochainement en salle", "en" : "Later"},
                        "search": { "community": "cinema", "record_type": "movie", "filter": "later"},
                    }
                ]
            }, {
                "code": "soundtracks",
                "staff_only": True,
                "default_genre": "selection",
                "with_selection": True,
                "recommandations": True,
                "genres_family": "soundtracks",
                "search": { "community": "music", "record_type": "album", "mode": "album"},
                "locales": { "fr": "Bandes originales", "en": "Soundtracks" }
            }, {
                "code": "bestmovies",
                "default_genre": "2014",
                "recommandations": True,
                "genres_family": "bestmovies-byyear",
                "search": { "community": "cinema", "record_type": "movie" },
                "locales": { "fr": "Meilleurs films", "en": "Best movies" }
            }, {
                "code": "shorts",
                "default_genre": "selection",
                "with_selection": True,
                "genres_family": "shortmovies",
                "search": { "community": "cinema", "record_type": "video", "mode": "shortmovie" },
                "locales": {"fr": "Courts", "en": "Shorts"},
            }, {
                "code": "showtimes",
                "comingsoon": True,
                "locales": { "fr": "Séances", "en": "Showtimes" }
            }, {
                "code": "all",
                "default_genre": "all",
                "staff_only": True,
                "genres_family": "movies",
                "minimum_results": 10,
                "search": {"community": "cinema", "record_type": "movie", "sort": "metadata.basicinfos.release_date"},
                "locales": { "fr": "Tous les films", "en": "All movies" },
                "ignore": True,
            }]
    }, {
        "code": "fashion",
        "locales": { "fr": "Mode", "en": "Fashion"},
        "welcome": {
            "boxes": [ {
                    "locale": { "fr": "Focus sur", "en": "Focus on" },
                    "boxtype": "fullsize",
                    "records": {
                        "main": { "type": ["video"], "category": "offcatwalk", "recommandations": "hidden-profile", "nb_items": 1 }
                    }
                }, {
                    "locale": { "fr": "Mode Femme", "en": "Women's Fashion" },
                    "params": {
                        "link": { "fr": "La mode féminine en Images", "en": "Discover Women's Fashion Images" },
                        "target": "fashion/woman/selection/",
                    },
                    "boxtype": "recobox",
                    "records": {
                        "bottom": { "type": ["image"], "category": "woman", "recommandations": "selection-bottom", "nb_items": 2 }
                    }
                }, {
                    "locale": { "fr": "En Coulisses", "en": "Off Catwalk" },
                    "params": {
                        "link": { "fr": "Les éditos Mode en vidéos", "en": "Discover editorial Videos" },
                        "target": "fashion/offcatwalk/editorials",
                    },
                    "boxtype": "fullsize",
                    "records": {
                        "main": { "type": ["video"], "category": "offcatwalk", "recommandations": "selection-top", "nb_items": 1 }
                    }
                }, {
                    "locale": { "fr": "Mode Homme", "en": "Men's fashion" },
                    "params": {
                        "link": { "fr": "La mode masculine en Images", "en": "Discover Men's Fashion Images" },
                        "target": "fashion/man/selection/",
                    },
                    "boxtype": "recobox",
                    "records": {
                        "bottom": { "type": ["image"], "category": "man", "recommandations": "selection-bottom", "nb_items": 2 }
                    }
                }, {
                    "locale": { "fr": "En Coulisses", "en": "Off Catwalk" },
                    "boxtype": "fullsize",
                    "params": {
                        "link": { "fr": "Brand Contents", "en": "Brand Contents" },
                        "target": "fashion/offcatwalk/brandcontents/",
                    },
                    "records": {
                        "main": { "type": ["video"], "category": "showpresentation", "recommandations": "selection-top", "nb_items": 1 }
                    }
                }, {
                    "locale": { "fr": "Mode Femme", "en": "Women's Fashion" },
                    "boxtype": "recobox",
                    "params": {
                        "link": { "fr": "Notre sélection d'accessoires", "en": "Our Selection of Accessories" },
                        "target": "fashion/woman/accessories/",
                    },
                    "records": {
                        "bottom": { "type": ["image"], "category": "woman", "recommandations": "accessories-bottom", "nb_items": 2 }
                    }
                }, {
                    "locale": { "fr": "Inspirez vous", "en": "Get inspired" },
                    "boxtype": "discoveralso",
                    "params": {
                        "readytowearwoman": {
                            "link": { "fr": "Prêt-à-Porter Femme", "en": "Women's Ready-to-Wear" },
                            "template": "image",
                            "target": "fashion/woman/readytowear",
                        },
                        "readytowearman": {
                            "link": { "fr": "Prêt-à-Porter Homme", "en": "Men's Ready-to-Wear" },
                            "template": "image",
                            "target": "fashion/man/readytowear",
                        },
                        "couturewoman": {
                            "link": { "fr": "Couture", "en": "Couture" },
                            "template": "image",
                            "target": "fashion/woman/couture/",
                        },
                        "coutureman": {
                            "link": { "fr": "Les éditos Femme", "en": "Women's Editorials" },
                            "template": "image",
                            "target": "fashion/woman/editorials/",
                        }
                    },
                    "records": {
                        "readytowearwoman": { "type": ["image"], "category": "woman", "recommandations": "seealso-readytowearwoman", "nb_items": 2 },
                        "readytowearman":   { "type": ["image"], "category": "man",   "recommandations": "seealso-readytowearman",   "nb_items": 2 },
                        "couturewoman":     { "type": ["image"], "category": "woman", "recommandations": "seealso-couturewoman",     "nb_items": 2 },
                        "coutureman":       { "type": ["image"], "category": "man",   "recommandations": "seealso-coutureman",       "nb_items": 2 },
                    }
                }
            ],
        },


        "categories": [  {
                "code": "woman",
                "default_genre": "selection",
                "genres_family": "imagefashionwomen",
                "minimum_results": 20,
                "with_selection": True,
                "search": { "community": "fashion", "record_type": "image", "mode": "woman" },
                "locales": { "fr": "Femme", "en": "Woman" }
            }, {
                "code": "man",
                "default_genre": "selection",
                "with_selection": True,
                "genres_family": "imagefashionmen",
                "minimum_results": 20,
                "search": { "community": "fashion", "record_type": "image", "mode": "man" },
                "locales": { "fr": "Homme", "en": "Man" }
            }, {
                "code": "kid",
                "default_genre": "selection",
                "with_selection": True,
                "genres_family": "imagefashionkids",
                "minimum_results": 20,
                "search": { "community": "fashion", "record_type": "image", "mode": "kid" },
                "locales": { "fr": "Enfant", "en": "Kid" }
            }, {
                "code": "offcatwalk",
                "default_genre": "selection",
                "with_selection": True,
                "selection_conf": {
                        "record_type": ['video', 'image'],
                        "alternate": {"image": 10, "video": 2},
                        "search": {},#FIXME
                },
                "genres_family": "fashionoffcatwalk",
                "minimum_results": 20,
                "search": { "community": "fashion", "obj_model": "media", "mode": "offcatwalk" },
                "locales": { "fr": "Coulisses", "en": "Off catwalk" },
                "alternate": {"image": 10, "video": 2},
            }, {
                "code": "showpresentation",
                "default_genre": "selection",
                "with_selection": True,
                "genres_family": "videofashionshowpresentation",
                "minimum_results": 10,
                "search": { "community": "fashion", "record_type": "video", "mode": "showpresentation" },
                "locales": { "fr": "Défilés et présentations", "en": "Show & Presentation" }
            } ]
    } ]
