
$(document).ready(function() {
    $("#filters ." + location.pathname.split('/')[5]+' input').attr("checked", "checked").parent().attr("style", "font-weight: bold !important;");

    $('#items .take_untake_item a').click(take_untake_item_onclick);
    $('#items .take_untake_category a').click(take_untake_category_onclick);
    $('#items .validate a').click(validate_item_onclick);

    update_counters_html();
});


function send_request($elem, callback) {
    $.ajax({
        url: $elem.attr("href"),
        type: "GET",
        timeout: 3000,
        success: function(data, textStatus, jqXHR) {
            callback($elem, data);
            update_counters_html();
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert("An unexpected error happened. Please refresh the page.");
        },
    });
}


function update_counters_data(status_old, status_new) {
    var status = ["all", "mine", "untaken", "taken", "success", "failed"];

    for (var i = 0, imax = status.length; i < imax; ++i) {
        if (status_old == status[i]) {
            counters[status[i]] -= 1;

            if (status_old == 'mine')
                counters['taken'] -= 1;
        }

        if (status_new == status[i]) {
            counters[status[i]] += 1;

            if (status_new == 'mine')
                counters['taken'] += 1;
        }
    }
}


function update_counters_html() {
    var status = 0, i = 0, imax = 0, total = 0;

    status = ["success", "failed", "untested"];

    for (i = 0, imax = status.length; i < imax; ++i) {
        total += counters[status[i]];
    }

    for (i = 0, imax = status.length; i < imax; ++i) {
        var percent = Math.round(counters[status[i]]/total*100);
        $('#progressbar table .' + status[i]).css('width', percent);
        $('#progressbar div .' + status[i] + ' .number').text(counters[status[i]]);
    }

    status = ["all", "mine", "untaken", "taken", "success", "failed"];

    for (i = 0, imax = status.length; i < imax; ++i) {
        $('#filters .' + status[i] + ' .number').text(counters[status[i]]);
    }

}


/*
    take untake item
*/

function take_untake_item_onclick() {
    send_request($(this), take_untake_item_update);
    return false;
}


function take_untake_item_update($elem, data) {
    var status_old = $elem.attr("data-status"), status_new = '';
    var $parent_elem = $elem.parent();

    if (status_old == 'untaken')
        status_new = 'mine';
    else
        status_new = 'untaken';

    update_counters_data(status_old, status_new);

    $parent_elem.html(data);
    $parent_elem.find('a').click(take_untake_item_onclick);
}


/*
    take untake category
*/

function take_untake_category_onclick() {
    send_request($(this), take_untake_category_update);
    return false;
}

function take_untake_category_update($elem, data) {
    $parent_elem = $elem.closest('table');
    var $elems = $parent_elem.find('.take_untake_item');

    /* clear take / untake data */
    for (var i = 0, imax = $elems.length; i < imax; ++i) {
        var status_old = $($elems[i]).find('a').attr('data-status'), status_new = '';

        if ($elem.parent().hasClass('take'))
            status_new = 'mine';
        else
            status_new = 'untaken';

        update_counters_data(status_old, status_new);

    }

    /* update html */
    $parent_elem.html(data);
    $parent_elem.find('.take_untake_item a').click(take_untake_item_onclick);
    $parent_elem.find('.take_untake_category a').click(take_untake_category_onclick);
    $parent_elem.find('.validate a').click(validate_item_onclick);
}


/*
    validate
*/

function validate_item_onclick() {
    send_request($(this), validate_item_update);
    return false;
}


function validate_item_update($elem, data) {
    var status_old = $elem.attr("data-status-old");
    var status_new = $elem.attr("data-status-new");
    var $parent_elem = $elem.parent();

    update_counters_data(status_old, status_new);

    $parent_elem.html(data);
    $parent_elem.find('a').click(validate_item_onclick);
}
