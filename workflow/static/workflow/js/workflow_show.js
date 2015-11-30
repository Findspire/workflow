'use strict';
$(document).ready(function() {
    $("#filters ." + location.pathname.split("/")[5]+" input").attr("checked", "checked").parent().attr("style", "font-weight: bold !important;");
    $("#items .validate a").each(function(){
        $(this).click(validate_item_onclick);
    });
    $("#workflow_add_item a").click(modal_onclick);
    $(".workflow_add_category").click(modal_onclick);
    $("a[data-target='pop-up']").click(popupShow);
    $(".pop-up .close").click(popupClose);  
    $(".take_untake_item a").click(takeItem);
    $(".take_untake_item a.close").click(untakeItem);
    $("table #sortable").each(function(){
        $(this).sortable({
            items: '.item_list',
            stop: onDragStop,
        }).disableSelection();
    });
    $(".tooltip").tooltip({
        position: { my: "left+15 center", at: "right center" }
    });
    $("#modal_background").click(modal_hide);

});

function popupData(popup){
    var $popup = $(popup),
        $ul = $popup.find('dl');

    $ul.empty();
    $.getJSON($popup.data('url'), function(data){
        var re = new RegExp("((((http|https):\/\/)?(www\.)?)?([a-zA-Z0-9;/?:@&=+$-])*(\.(fr|com|eu|org|net|edu|gouv|co|paris)){1}(\/[a-zA-Z0-9;/?:@&=+$-_!~*'()]+)?)");
        $.each(data, function(key, val){
            var words = val.text.split(' ');
            for(var i in words){
                var word = String(words[i]);
                if(word.match(re)){
                    if(!word.startsWith('http')){
                        word = 'http://' + word;
                        words[i] = word;
                    }
                }
            }
            val.text = words.join(' ');
            var text = val.text.replace(re, '<a class="link" target="_blank" href="$&">$&</a>');
            $ul.append('<dt class="title"><b>'+ val.username + ' ' + $.datepicker.formatDate('dd/mm', new Date(val.date))  + '</b></dt>')
               .append('<dd class="text">'+ text + '</dd>');
        });
    });
}

function popupShow(){
    var $element = $($(this).next());
    $element.addClass('active').draggable();
    popupData($element);
}

function popupClose(){
    $(this).closest('.pop-up').removeClass('active');
    return false;
}

function onDragStop(event, ui){
    var item = $(ui.item).data("itemPk");
    var related = $(ui.item).next().data("itemPk");
    setItemPosition(related, item);
}

function setItemPosition(afterId, taskId){
    if(afterId){
        var url = "/workflow/drag-item/" + taskId + "/" + afterId + "/";
    }else{
        var url = "/workflow/drag-item/" + taskId + "/";  
    }
    var dfd = $.post(url);
    dfd.fail(function(jqXHR, textStatus){
        console.log(textStatus);
    });
}     


function send_request($elem){
    var dfd = $.get($elem.attr("href"));
    dfd.fail(function(jqXHR){
            alert(jqXHR.responseText);
    });
    return dfd;
}

function sendPutRequest(url, data){
    var dfd = $.ajax({
        url: url,
        type: 'PUT',
        data: data,
    });
    dfd.fail(function(jqXHR){
        console.log(jqXHR.responseText);
    });
    return dfd;
}

function updateProgressBar(){
    var $bar = $('.progress'),
        successBar = $bar.find('.progress-bar-success'),
        untestedBar = $bar.find('.progress-bar-untested'),
        failedBar = $bar.find('.progress-bar-danger');

    var counts = {
        0: 0, // Untested items
        1: 0, // Success items
        2: 0 // Failed items
    },
    total = 0;

    var $trs = $('.item_list');
    $trs.each(function() {
        counts[this.getAttribute('data-status')] += 1;
    });
    total = $trs.length; 
    successPercent = (counts[1] * 100 )/ total;
    untestedPercent = (counts[0] * 100 )/ total;
    failedPercent = (counts[2] * 100 )/ total;

    successBar.css('width', successPercent + '%').text(Math.round(successPercent) + '%');
    untestedBar.css('width', untestedPercent + '%').text(Math.round(untestedPercent) + '%');
    failedBar.css('width', failedPercent + '%').text(Math.round(failedPercent) + '%');
    updateCounters(counts);
}

function updateCounters(counts){
    $('.square.success .number').text(counts[1]);
    $('.square.untested .number').text(counts[0]);
    $('.square.failed .number').text(counts[2]);
    $('#filters .success .number').text(counts[1]);
    $('#filters .failed .number').text(counts[2]);
}

function takeItem(){
    var elem = $(this);
    var username = elem.closest('table').data('username');
    var item_pk = elem.closest('.item_list').data('item-pk');
    if(elem.hasClass('not-take')){
        var dfd = sendPutRequest(
            "/api/item/" + item_pk + "/take/" + username + "/",
            {username: username, item_pk: item_pk}
        );
        dfd.done(function(){
            elem.removeClass('not-take');
            var link = $('<a class="close untake"><span class="glyphicon glyphicon-remove"></span></a>');
            elem.closest('.take_untake_item').html(username + link[0].outerHTML);
            $('.untake').click(untakeItem);
        });
    }
}

function untakeItem(){
    var elem = $(this);
    var item_pk = elem.closest('.item_list').data('item-pk');
    if(!elem.hasClass('not-take')){
        var dfd = sendPutRequest(
            "/api/item/" + item_pk + "/untake/",
            {item_pk: item_pk}
        );
        dfd.done(function(){
            var link = $('<a class="not-take">Take</a>');
            elem.closest('.take_untake_item').html(link);
            link.click(takeItem);
        });
    }

}

function validate_item_onclick() {
    var elem = $(this);
    var url = $(elem).data('url');
    $.get(url)
        .done(function(data){
            var status_old = data.status_old;
            var status_new = data.validation;
            $(elem).closest('tr').attr('data-status', status_new);
            $(elem).closest('td').find('span.validated').removeClass('validated');
            $(elem).find('span').addClass('validated');
            $(elem).closest('td').find('span.last_modification').text(moment(data.updated_at).format('D/MM/YYYY HH:mm'));

            updateProgressBar();
        })
        .fail(function(jqXHR){
            alert(jqXHR.responseText);
        });
    return false;
}

function modal_onclick() {
    $elem = $(this)
    send_request($elem)
        .done(function(data){ 
            modal_callback($elem, data); 
        });
    return false;
}

function modal_callback($elem, data) {
    var $content = $($.trim(data)).filter("#content");
    $content.find("form").attr("action", $elem.attr("href")); // set the correct target url

    $("body #modal_content").html($content.html()+'<a href="#" class="close_modal">&times;</a>');
    $("#modal_content form :submit").click(modal_form_submit_onclick);

    // callback to close the modal
    $("#modal_background").click(modal_hide);
    $("#modal_content .close_modal").click(modal_hide);

    modal_show();
}

function modal_show() {
    $("#modal_content").css("top", window.scrollY);
    $("#modal_background").show();
    $("#modal_content").show();
    return false;
}

function modal_hide() {
    $("#modal_background").hide();
    $("#modal_content").hide();
    return false;
}


function modal_form_submit_onclick() {
    var f = $("#modal_content form");
    $.post(f.attr("action"), f.serialize())
        .done(function(data, textStatus, jqXHR){
            if (jqXHR.getResponseHeader("Content-Type") === "text/html; charset=utf-8") {
                /* post failed, show the form again */
                modal_callback($("#modal_content form").attr("action"), data);
            }
            else {
                /* post successfull (this is supposed to be an empty json response) */

                modal_hide();

                var cat_id = f.find("select :selected").attr("value");

                if (typeof cat_id === "undefined") {
                    /* new category, we must reload the whole page to show it */
                    location.reload();
                }
                else {
                    /* category already exist, just refresh it */
                    counters["all"] += 1;
                    counters["untaken"] += 1;
                    counters["untested"] += 1;
                    $("#take_untake_category_"+cat_id + "_show a").click();
                }
            }
        })
        .fail(function(jqXHR){
            console.log(jqXHR.responseText);            
        });
    return false;
}
