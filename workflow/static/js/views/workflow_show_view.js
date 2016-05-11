define(['backbone'], 
function(Backbone) {
    var WorkflowShowView = Backbone.View.extend({
        
        username: document.getElementsByTagName('body')[0].getAttribute('data-username'),
        
        events: {
            'click .take a': 'takeAllItems',
            'click .untake a': 'untakeAllItems'
        },
        
        initialize: function() {
        },

        takeAllItems: function(e) {
            e.preventDefault();
            $.get(e.target.href)
             .success(function() {
                 console.log('Test');
                var $elemId = $(e.currentTarget).closest('table'); 
                $elemId.css('backgroundColor', 'red');
                //window.location.href = document.URL + elemId;
             });
        }
    });

    return WorkflowShowView;
});

