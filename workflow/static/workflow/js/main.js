require.config({
    baseUrl: '/static',

    paths: {
        'backbone': 'components/backbone/backbone-min',
        'underscore': 'components/underscore/underscore-min',
        'jquery': 'components/jquery/dist/jquery.min',
        'jqueryUi': 'components/jquery-ui/jquery-ui.min',
        'alertify': 'components/alertify/alertify.min',
        'bootstrap': 'components/bootstrap/dist/js/bootstrap.min',
        'moment': 'components/moment/min/moment.min',
        'workflow': 'workflow/js/workflow',
        'dashboard': 'workflow/js/dashboard'
    },

    shim: {
        backbone: {
            deps: ['jquery', 'underscore'],
            exports: 'Backbone'
        },
        undescore: {
            exports: '_'
        },
        jquery: {
            exports: '$'
        },
        jqueryUi: {
            deps: ['jquery']
        },
        bootstrap: {
            deps: ['jquery']
        },
        workflow: {
            deps: ['jquery']
        }
    }
});

require(['workflow', 'dashboard']);
