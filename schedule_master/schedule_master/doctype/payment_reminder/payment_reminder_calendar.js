// Copyright (c) 2019, Hardik Gadesha and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment Reminder', {
	refresh: function(frm) {

	}
});

frappe.views.calendar["Payment Reminder"] = {
	field_map: {
		"start": "next_reminder_date",
		"end": "next_reminder_date",
		"id": "parent",
		"title": "remarks",
		"color": "color",
		"allDay": "allDay"
	},
	get_events_method: "frappe.desk.calendar.get_events"
}
