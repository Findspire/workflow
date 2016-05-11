define(['jquery', 'underscore', 'alertifyjs'], 
function($, _, alertify) {
    var dsb = {};
    
    $(function() {
      dsb.path = window.location.pathname;
      dsb.dom = {};
      dsb.dom.sidebar = {};
      dsb.dom.sidebar.btnLink = $('.sidebar li a');
      dsb.dom.filterSelect = $('.filters select');
      dsb.dom.workflowPanel = $('.workflow .panel-body');
      dsb.templates = {};
      dsb.templates.workflowPanel = $('#template_workflow_panel');
      dsb.templates.itemsDetailsPanel = $('#template_users_items_details');
      dsb.templates.categoryDetailsPanel = $('#template_users_categories_details');
      $('.filters select').on('change', filtersUsersChange);
      $.each(dsb.dom.sidebar.btnLink, function(i, value) {
        $(value).on('click', function(e){sidebarEvent(e)})
      });

      dsb.ajax = {};
      dsb.ajax.send = function(url, data, type) {
          var dfd = $.ajax({
              url: url,
              type: type,
              data: data,
          });
          dfd.fail(function(jqXHR){
              console.log(jqXHR.responseText);
          });
          return dfd;
      }

      dsb.ajax.get = function(url, data) {
          return dsb.ajax.send(url, data, 'GET');
      };

      dsb.ajax.put = function(url, data) {
          return dsb.ajax.send(url, data, 'PUT');
      };

      dsb.ajax.patch = function(url, data) {
          return dsb.ajax.send(url, data, 'PATCH');
      };

      dsb.ajax.post = function(url, data) {
          return dsb.ajax.send(url, data, 'POST');
      };

      dsb.ajax.delete = function(url, data) {
          return dsb.ajax.send(url, data, 'DELETE');
      };

      displayUsersPage();
    });

    function sidebarEvent(e) {
      var $elem = $(e.currentTarget)
      $elem.closest('ul').find('.active').removeClass('active');
      if($elem.hasClass('users-link')) {
        displayUsersPage();
      } else if ($elem.hasClass('projects-link')) {
        alertify.error("Project view : Coming soon !");
      } else if ($elem.hasClass('ideas-link')) {
        alertify.error("Ideas Box : Coming soon !");
      } else if ($elem.hasClass('question-link')) {
        displayQuestionPage();
      } else {
        displayUsersPage();
      }
    }

    function displayUsersPage() {
      var url = '/api/persons/';
      $('.filters').show();
      $('.users-link .btn').addClass('active')
      workflowPanelFilterSelect(url, 'username');
      $('.dashboard .container').load('/dashboard/users/');
    }

    function displayProjectsPage() {
      var url = '/api/projects/';
      $('.projects-link .btn').addClass('active');
      workflowPanelFilterSelect(url, 'name');
      $('.dashboard .container').load('/dashboard/projects/');
    }

    function displayQuestionPage() {
      $('.filters').hide();
      $('.question-link .btn').addClass('active');
      $('.dashboard .container').load('/dashboard/changelog/');
    }
    function workflowPanelFilterSelect(url, attr) {
      dsb.ajax.get(url, null)
          .done(function(data){
            dsb.dom.filterSelect.empty();
            $.each(data, function(i, value) {
              var val = $(value).attr(attr);
              dsb.dom.filterSelect.append(new Option(val, value.id));
            });
          });
    }


    function workflowAppendPanel(data) {;
      var panel = $('.workflow .panel-body');
      workflowTpl = _.template(dsb.templates.workflowPanel.html().trim());
      panel.append(workflowTpl(data));
    }

    function filtersUsersChange() {
      var val = $(this).val(),
          url = '/api/persons/' + val + '/workflow/',
          dfd = dsb.ajax.get(url, null),
          panel = $('.workflow .panel-body').empty();
      $('.tasks-details .panel-body').empty();
      dfd.done(function(data){
        $.each(data, function(i, value){
          workflowAppendPanel(value);
        });
        $('.workflow article').on('click', function() {
          displayWorkflowDetails(this.getAttribute('data-workflow-pk'));
        });
      });
    }

    function displayWorkflowDetails(workflowPk) {
      var personPk = $('.filters select').val(),
          url = '/api/workflow/mine/' + personPk + '/' + workflowPk + '/',
          dfd = dsb.ajax.get(url, null);
      dfd.done(function(data){
        $('.tasks-details .panel-body').empty();
        var items = [];
        $.each(data, function(i, value) {
          items.push(value);
        });
        items = _.groupBy(items, function(item) { return item.category.name });
        $.each(items, function(i, category) {
          appendCategoryToDetails({'name':i });
          $.each(category, function(i, item){
            appendItemToDetails(item);
          });
        });
      });
    }

    function appendCategoryToDetails(data) {
      var categoryTpl = _.template(dsb.templates.categoryDetailsPanel.html().trim()),
          parsedTpl = categoryTpl(data);
      $('.tasks-details .panel-body').append(parsedTpl);
    }

    function appendItemToDetails(data) {
      var itemTpl = _.template(dsb.templates.itemsDetailsPanel.html().trim()),
          parsedTpl = itemTpl(data);
      $('.tasks-details .panel-body').append(parsedTpl);
    }
});
