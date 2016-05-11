define(['backbone'], 
function(Backbone) {
    var WorkflowShowView = Backbone.View.extend({
        
        username: document.getElementsByTagName('body')[0].getAttribute('data-username'),
        
        events: {
            'click .take a': '',
            'click .untake a': ''
        },
        
        initialize: function() {
        },

        takeAllItems: function(e) {
        }
    });

    return WorkflowShowView;
});

