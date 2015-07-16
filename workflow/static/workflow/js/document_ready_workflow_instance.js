$(document).ready(function() {
	$("#progress_bar").append(progressbar);
	update_statistics_progressbar();
	update_statistics_filters();
	$(".category_workflow a.shortcut").click(update_item_shortcut);
	$(".category_workflow td.take-item").click( update_item_add_owner);
	$(".category_workflow td.untake-item").click( update_item_reset_owner);
	$("a.untake-group").click( update_whole_group_reset_owner);
	$("a.take-group").click( update_whole_group_add_owner);
});
