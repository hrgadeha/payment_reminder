// Copyright (c) 2019, Hardik Gadesha and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment Reminder', {
	refresh: function(frm) {

	}
});

cur_frm.add_fetch('next_follow_up_by', 'mobile_no', 'contact_number')

frappe.ui.form.on("Payment Reminder", {
  get_details: function(frm) {
	cur_frm.clear_table("payment_reminder_table");
	cur_frm.clear_table("contact_table");
	cur_frm.refresh_fields();
	var total = 0;
	var days = 0;

	if(frm.doc.party){

    frappe.call({
    "method": "schedule_master.schedule_master.doctype.payment_reminder.payment_reminder.getOverdue",
args: {
party: frm.doc.party
},
callback:function(r){
		var len=r.message.length;
	        for (var i=0;i<len;i++){

//		console.log(r.message[i][4]);
	        var row = frm.add_child("payment_reminder_table");
		row.invoice = r.message[i][0];
		row.posting_date = r.message[i][1];
		row.date = r.message[i][2];
		row.status = r.message[i][3];
		row.outstanding_amount = r.message[i][4];
		row.days = r.message[i][5];
		total = total + r.message[i][4];
		days = days + r.message[i][5];
	}
		cur_frm.refresh();
		frm.set_value("total_outstanding_amount", total);
		frm.set_value("total_overdue_days", days);
	}
    });
}

	frappe.call({
    "method": "schedule_master.schedule_master.doctype.payment_reminder.payment_reminder.getContact",
args: {
party: frm.doc.party
},
callback:function(r){
	var len=r.message.length;
	for (var i=0;i<len;i++){
//		console.log(r.message);
	        var row_1 = frm.add_child("contact_table");
		row_1.name1 = r.message[i][0];
		row_1.department = r.message[i][1];
		row_1.designation = r.message[i][2];
		row_1.number = r.message[i][3];
		row_1.email = r.message[i][4];
		frm.set_value("contact_email",r.message[i][4]);
	}
		cur_frm.refresh();
	}
    });
}
});

frappe.ui.form.on('Payment Reminder', 'send_sms', function(frm){
	var date = frm.doc.next_reminder_date;
	var p = date.split(/\D/g)
	var new_date = [p[2],p[1],p[0] ].join("-")
  	var message = frm.doc.follow_up_by + ' Assign You Payment Follow Up ' + frm.doc.name + ' On Date : ' + new_date;

console.log(message);
  frappe.call({
    method: "frappe.core.doctype.sms_settings.sms_settings.send_sms",
    args: {
      receiver_list: [frm.doc.contact_number],
      msg: message,
    },
    callback: function(r) {
      if(r.exc) {msgprint(r.exc); return;}
    }
  });
})


frappe.ui.form.on("Payment Reminder Table", {
	"payment_reminder_table_remove": function(frm, cdt, cdn) {
		cur_frm.refresh();
		cur_frm.refresh_fields();
		var d = locals[cdt][cdn];
		var total = 0;
		var sales_invoice = frm.doc.payment_reminder_table;
//		console.log(total)

   	for(var i in sales_invoice) {
		total = total + sales_invoice[i].outstanding_amount;
		frm.set_value("total_outstanding_amount", total);
	}
}
});


frappe.ui.form.on('Payment Reminder', {
    setup: function(frm) {
	frm.set_query('company_address', function(doc) {
			return {
				query: 'frappe.contacts.doctype.address.address.address_query',
				filters: {
					link_doctype: 'Company',
					link_name: doc.company
				}
			};
		});
    }
});

frappe.ui.form.on('Payment Reminder', {
    setup: function(frm) {
	frm.set_query('customer_address', function(doc) {
			return {
				query: 'frappe.contacts.doctype.address.address.address_query',
				filters: {
					link_doctype: 'Customer',
					link_name: doc.party
				}
			};
		});
    }
});

/*
frappe.ui.form.on("Payment Reminder", {
  get_details: function(frm) {
    frappe.call({
    "method": "schedule_master.schedule_master.doctype.payment_reminder.payment_reminder.getPDC",
args: {
party: frm.doc.party
},
callback:function(r){
        console.log(r.message);
		frm.set_value("pdc_cheque_amount", r.message[0][1]);
	}
    });
}
});
*/

/*frappe.ui.form.on('Payment Reminder',  'get_details',  function(frm) {
    frm.set_value("receivable_amount", frm.doc.total_outstanding_amount - frm.doc.pdc_cheque_amount);
});*/

frappe.ui.form.on("Contact Table", {
        "mail": function(frm, cdt, cdn) {
                var d = locals[cdt][cdn];
         if(d.mail == 1){
                frm.set_value("contact_email", d.email);
        }
}
});
