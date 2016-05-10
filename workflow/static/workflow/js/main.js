require.config({
    baseUrl: '/static',

    paths: {
        'backbone': 'components/backbone/backbone-min',
        'underscore': 'components/underscore/underscore-min',
        'jquery': 'components/jquery/dist/jquery.min',
        'jquery-ui': 'components/jquery-ui/jquery-ui.min',
        'alertifyjs': 'components/alertify.js/dist/js/alertify',
        'bootstrap': 'components/bootstrap/dist/js/bootstrap.min',
        'moment': 'components/moment/min/moment.min',
        'workflow': 'workflow/js/workflow',
        'dashboard': 'workflow/js/dashboard'
    },

    shim: {
        'backbone': {
            deps: ['jquery', 'underscore'],
            exports: 'Backbone'
        },
        'undescore': {
            exports: '_'
        },
        'jquery': {
            exports: '$'
        },
        'jquery-ui': {
            deps: ['jquery'],
            exports: '$' 
        },

        'bootstrap': ['jquery'],
    },
});

require(['bootstrap', 'workflow', 'dashboard']);
