define(['backbone', 
        'js/views/workflow_show_view'],
function(Backbone, WorkflowShowView) {
    var WorkflowRouter = Backbone.Router.extend({
        routes: {
            "workflow/workflow/show/:id/:display/": "workflowShow",
        },

        workflowShow: function() {
            new WorkflowShowView({
                el: $('#items')
           });
        }
    });

    return WorkflowRouter;
});
