# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import utils

def get_notification_config():
	notifications = { "for_doctype": 
		{
			"Payment Reminder": "schedule_master.notifications.get_things_todo",
		}
	}
	
	return notifications

def get_things_todo(as_list=False):
	"""Returns a count of incomplete todos"""
	data = frappe.get_list("Payment Reminder",
		fields=["name", "description"] if as_list else "count(*)",
		filters=[["Payment Reminder", "status", "=", "Open"],
			 ["Payment Reminder", "next_reminder_date", "=", utils.today()],
			 ["Payment Reminder", "next_follow_up_by", "=", frappe.session.user]],
		as_list=True)

	if as_list:
		return data
	else:
		return data[0][0]
