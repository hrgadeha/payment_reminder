from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

@frappe.whitelist(allow_guest=True)
def sendmail():
	customer_list = frappe.db.sql("""select customer,customer_name,contact_email,sum(outstanding_amount),contact_mobile,contact_display
			from `tabSales Invoice` where docstatus = 1 and status = 'Overdue' group by customer;""")
	for customer_obj in customer_list:
		total = 0.0
		customer = customer_obj[0]
		customer_name = customer_obj[1]
		total = total + customer_obj[3]
		contact_name = customer_obj[5]
		contact_number = customer_obj[4]
		content = "<h4>Kind attention, "+ customer_name +"</h4><p>This is to remind you that, your following sales invoice payment is overdue. Total outstanding amount is "+str(total)+". Please pay as soon as possible.</p>"
		content = content + "<p><b>Contact Person : "+ str(contact_name) +"</b></p><p><b>Contact No : "+ str(contact_number) +"</b></p>"
		content = content + "<table class='table table-bordered'><tr><th>Invoice</th><th>Posting Date</th><th>Due Date</th><th>Outstanding Amount</th><th>Overdue Days</th></tr>"
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
		frappe.sendmail(recipients=[recipient],sender="info@shreelight.in",cc="admin@shreelight.com",
		subject="Payment Reminder", content=content)


@frappe.whitelist(allow_guest=True)
def send_draft():
	content = "<h4>Hello, </h4><p>Purchase Order</p><table class='table table-bordered'><tr><th>PO Number</th><th>Supplier</th><th>Required Date</th><th>Prepared By</th></tr>"
	po = frappe.db.sql("""select name,supplier_name,schedule_date,owner from `tabPurchase Order` where docstatus = 0;""")
	for i in po:
		date = str(i[2].strftime('%d/%m/%Y'))
		content = content + "<tr><td>"+i[0]+"</td><td>"+i[1]+"</td><td>"+date+"</td><td>"+i[3]+"</td></tr>"
	content = content + "</table>"

	content = content + "<p>Sales Order</p><table class='table table-bordered'><tr><th>SO Number</th><th>Customer</th><th>Delivery Date</th><th>Prepared By</th></tr>"
	so = frappe.db.sql("""select name,customer_name,delivery_date,owner from `tabSales Order` where docstatus = 0;""")
	for d in so:
		so_date = str(d[2].strftime('%d/%m/%Y'))
		content = content + "<tr><td>"+d[0]+"</td><td>"+d[1]+"</td><td>"+so_date+"</td><td>"+d[3]+"</td></tr>"
	content = content + "</table>"

	content = content + "<p>Delivery Note</p><table class='table table-bordered'><tr><th>DN Number</th><th>Customer</th><th>Date</th><th>Prepared By</th></tr>"
	dn = frappe.db.sql("""select name,customer_name,posting_date,owner from `tabDelivery Note` where docstatus = 0;""")
	for dl in dn:
		dn_date = str(dl[2].strftime('%d/%m/%Y'))
		content = content + "<tr><td>"+dl[0]+"</td><td>"+dl[1]+"</td><td>"+dn_date+"</td><td>"+dl[3]+"</td></tr>"
	content = content + "</table>"


	content = content + "<p>Purchase Receipt</p><table class='table table-bordered'><tr><th>PR Number</th><th>Supplier</th><th>Date</th><th>Prepared By</th></tr>"
	pr = frappe.db.sql("""select name,supplier_name,posting_date,owner from `tabPurchase Receipt` where docstatus = 0;""")
	for prn in pr:
		pr_date = str(prn[2].strftime('%d/%m/%Y'))
		content = content + "<tr><td>"+prn[0]+"</td><td>"+prn[1]+"</td><td>"+pr_date+"</td><td>"+prn[3]+"</td></tr>"
	content = content + "</table>"

	content = content + "<p>Sales Invoice</p><table class='table table-bordered'><tr><th>SI Number</th><th>Customer</th><th>Date</th><th>Prepared By</th></tr>"
	si = frappe.db.sql("""select name,customer_name,posting_date,owner from `tabSales Invoice` where docstatus = 0;""")
	for s in si:
		si_date = str(s[2].strftime('%d/%m/%Y'))
		content = content + "<tr><td>"+s[0]+"</td><td>"+s[1]+"</td><td>"+si_date+"</td><td>"+s[3]+"</td></tr>"
	content = content + "</table>"

	content = content + "<p>Purchase Invoice</p><table class='table table-bordered'><tr><th>PI Number</th><th>Supplier</th><th>Date</th><th>Prepared By</th></tr>"
	pi = frappe.db.sql("""select name,supplier_name,posting_date,owner from `tabPurchase Invoice` where status = "Draft";""")
	for p in pi:
		pi_date = str(p[2].strftime('%d/%m/%Y'))
		content = content + "<tr><td>"+p[0]+"</td><td>"+p[1]+"</td><td>"+pi_date+"</td><td>"+p[3]+"</td></tr>"
	content = content + "</table>"

	content = content + "<p>Stock Transfer</p><table class='table table-bordered'><tr><th>Number</th><th>SO</th><th>Date</th><th>Prepared By</th></tr>"
	st = frappe.db.sql("""select name,sales_order,posting_date,owner from `tabStock Entry` 
			where docstatus = 0 and stock_entry_type = "Reservation of Stock";""")
	for se in st:
		st_date = str(se[2].strftime('%d/%m/%Y'))
		content = content + "<tr><td>"+se[0]+"</td><td>"+se[1]+"</td><td>"+st_date+"</td><td>"+se[3]+"</td></tr>"
	content = content + "</table>"

	content = content + "<p>Material Request</p><table class='table table-bordered'><tr><th>Number</th><th>SO</th><th>Date</th><th>Prepared By</th></tr>"
	mr = frappe.db.sql("""select name,against_sales_order,schedule_date,owner from `tabMaterial Request` 
			where docstatus = 0 and workflow_state = "Open";""")
	for m in mr:
		mr_date = str(m[2].strftime('%d/%m/%Y'))
		content = content + "<tr><td>"+str(m[0])+"</td><td>"+str(m[1])+"</td><td>"+str(mr_date)+"</td><td>"+m[3]+"</td></tr>"
	content = content + "</table>"

	recipient = "info@shreelight.com"
	frappe.sendmail(recipients=[recipient],
	sender="info@shreelight.in",
	subject="Draft Entry", content=content)
