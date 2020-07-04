# -*- coding: utf-8 -*-
# Copyright (c) 2019, Hardik Gadesha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class PaymentReminder(Document):
	pass

@frappe.whitelist(allow_guest=True)
def getOverdue(party):
	data = frappe.db.sql("""select name,posting_date,due_date,status,outstanding_amount,DATEDIFF(CURDATE(),due_date) 
			from `tabSales Invoice` where status = 'Overdue' and customer = %s;""",(party),as_list=1)
	return data

@frappe.whitelist(allow_guest=True)
def getPDC(party):
        data = frappe.db.sql("""select name,paid_amount 
                        from `tabPayment Entry` where docstatus = 0 and party = %s and mode_of_payment = "PDC Cheque";""",(party),as_list=1)
        return data

@frappe.whitelist(allow_guest=True)
def getContact(party):
        data = frappe.db.sql("""select c.first_name,c.department,c.designation,c.mobile_no,c.email_id from `tabContact` c, 
				`tabDynamic Link` dl
				where c.name = dl.parent and dl.link_name = %s;""",(party),as_list=1)
        return data
