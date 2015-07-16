$(document).ready(function() {
	$("td a.shortcut").click(update_item_shortcut);
	$("td.take-item").click(update_item_add_owner);
	$("td.untake-item").click(update_item_reset_owner);
});
