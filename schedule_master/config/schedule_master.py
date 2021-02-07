from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Payment Reminder"),
			"items": [
				{
					"type": "doctype",
					"name": "Payment Reminder",
					"label": "Payment Reminder",
					"description": _("Payment Reminder"),
				}
			]
		}
	]
