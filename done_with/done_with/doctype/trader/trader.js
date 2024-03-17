// Copyright (c) 2024, Polito and contributors
// For license information, please see license.txt

frappe.ui.form.on('Trader', {
    onload: function (frm) {
        frm.set_query('make_bid', 'listed_item', () => {
            return {
                filters: {
                    "status": "Pending"
                }
            }
        })
      
    },
    refresh: function(frm) {
        // Add a custom event handler for the "Bid" button click
        // frm.fields_dict.check_items.$input.on('click', function() {
        //     // Redirect to 'Make Bid' doctype
        //     frappe.set_route('Form', 'Item on Sale');
        // });
        frappe.call({
            method: 'done_with.services.rest.listed_items',
            args: {
            },
            callback: function (r) {
                console.log(r.message)    
            }
        });
        frappe.call({
            method: 'done_with.services.rest.received_bids',
            args: {
            },
            callback: function (r) {
                console.log(r.message) 
            }
        });
    },
    
    // validate: function(frm) {
		

	// },
    
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

frappe.ui.form.on('Offer Request', {
    item(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        let email = frm.doc.trader_email;
        let contact=frm.doc.trader_contact;
        let item_name=row.item
       
     
        frappe.call({
            method: 'done_with.services.rest.bidding_form',
            args: {
                "email": email,
                "contact":contact
            },
            callback: function (r) {
                if (r.message) {
                    frappe.model.set_value(cdt, cdn, {
                        bidder_email: r.message[0]
					
                    });
					frappe.model.set_value(cdt, cdn, {
                        contact: r.message[1]
                    });

                }
            }
        });
        frappe.call({
            method: 'done_with.services.rest.check_bidder',
            args: {
                "email": email,
                "item_name":item_name
            },
            callback: function (r) {
                if (r.message) {
                    frappe.msgprint('You can\'t bid on your own item.');
                    frappe.validate = false;
                }
                else {
                    frappe.validate = true;
                }
            }
        });
		

    },


});


    

