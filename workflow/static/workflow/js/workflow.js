
function progressbar_update(counters, percent) {
    var content = '';
    var items = ['success', 'failed', 'untested'];
    var index = 0;

    content += '<table>';
    content += '<tr>';

    // progress bar
    for (index in items) {
        content += '<td class="'+items[index]+'" style="width: '+percent[items[index]]+'%"></td>';
    }
    content += '<td style="width: auto; text-align: left; padding-left: 4px;">'+(percent['success']+percent['failed'])+'% tested</td>';
    content += '</tr>';
    content += '</table>';

    // stats
    content += '<div>';
    content += '<ul>';
    for (index in items) {
        content += '<li><span class="'+items[index]+'"></span>'+items[index]+': '+counters[items[index]]+'</li>';
    }
    content += '</ul>';
    content += '</div>';

    $('#progressbar').html(content);
}

function filters_update(counters) {
    var items = ['all', 'mine', 'taken', 'untaken', 'success', 'failed'];
    var index;

    for (index in items) {
        var item = items[index];
        $('#filters .'+item+' span').html(item+" items (" + counters[item] + ")");
    }

    $("#filters ." + location.pathname.split('/')[5]+' input').attr("checked", "checked").parent().attr("style", "font-weight: bold;");
}
