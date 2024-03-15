// Copyright (c) 2024, Polito and contributors
// For license information, please see license.txt

frappe.ui.form.on('Trader', {
	// validate: function(frm) {
		

	// }
});



frappe.ui.form.on('List Item', {
    item_name(frm, cdt, cdn) {
        let item = locals[cdt][cdn];
        let email = frm.doc.trader_email;
       
     
        frappe.call({
            method: 'done_with.services.rest.list_item',
            args: {
                "email": email,
            },
            callback: function (r) {
                if (r.message) {
                    frappe.model.set_value(cdt, cdn, {
                        seller_id: r.message[0]
					
                    });
					frappe.model.set_value(cdt, cdn, {
                        date_listed: r.message[1]
                    });

                }
            }
        });
		

    },
});

    

