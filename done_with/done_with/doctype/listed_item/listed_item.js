// Copyright (c) 2024, Polito and contributors
// For license information, please see license.txt

frappe.ui.form.on('Listed Item', {
	refresh: function(frm) {

		frappe.call({
            method: 'done_with.services.rest.listed_items',
            args: {
            },
            callback: function (r) {
				console.log(r.message)
               
                
            }
        });
		
	}
});
