from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

@frappe.whitelist(allow_guest=True)
def sendmail():
	customer_list = frappe.db.sql("""select customer,customer_name,contact_email,sum(outstanding_amount) from `tabSales Invoice` 
			where docstatus = 1 and status = 'Overdue' group by customer;""")
	for customer_obj in customer_list:
		total = 0.0
		customer = customer_obj[0]
		customer_name = customer_obj[1]
		total = total + customer_obj[3]
		content = "<h4>Kind attention, "+ customer_name +"</h4><p>This is to remind you that, your following sales invoice payment is overdue. Total outstanding amount is "+str(total)+". Please pay as soon as possible.</p><table class='table table-bordered'><tr><td>Invoice</td><td>Posting Date</td><td>Due Date</td><td>Outstanding Amount</td><td>Overdue Days</td></tr>"
		invoice_list = frappe.db.sql("""select name,posting_date,due_date,outstanding_amount,DATEDIFF(CURDATE(),due_date) 
				from `tabSales Invoice` where docstatus = 1 and status = 'Overdue'
				and customer_name = %s;""",customer_name)
		for invoice_obj in invoice_list:
			invoice = invoice_obj[0]
			posting_date = str(invoice_obj[1].strftime('%d/%m/%Y'))
			due_date = str(invoice_obj[2].strftime('%d/%m/%Y'))
			grand_total = '{:20,.2f}'.format(invoice_obj[3])
			days = str(invoice_obj[4])
			content = content + "<tr><td>"+invoice+"</td><td>"+posting_date+"</td><td>"+due_date+"</td><td>"+grand_total+"</td><td>"+days+"</td></tr>"
		content = content + "</table><br><br><table><tr><td><b>RTGS / NEFT DETAILS : </b><br><b>NAME OF BANK : Induslnd Bank Ltd. </b><br><b>BRANCH ADDRESS :G.F. & F.F. GOLD CROFT, VISHWAS COLONY,</b><br><b>JETALPUR ROAD, VADODARA‐390005 ( GUJARAT )</b><br><b>PHONE NO : 0265‐2410750</b><br><br><b>ACCOUNT NAME : SHREELIGHT POWER PRIVATE LIMITED</b><br><b>BANK ACCOUNT NO : 650014032720</b><br><b>MICR CODE : 390234002</b><br><b>RTGS IFSC CODE : INDB0000017</b><br><b>NEFT IFSC CODE : INDB0000017</b></td></tr></table><br><br><br>From : Shreelight Power Pvt.Ltd<br>Ph : +91 265 2412551<br><b>UAN(MSME) : GJ24A0000958</b>"
		recipient = "info@shreelight.com"
		frappe.sendmail(recipients=[recipient],sender="support@shreelight.com",cc = "admin@shreelight.com",
		subject="Payment Reminder", content=content)
