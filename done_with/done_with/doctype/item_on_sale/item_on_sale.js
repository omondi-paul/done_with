// Copyright (c) 2024, Polito and contributors
// For license information, please see license.txt

// frappe.ui.form.on('Item on Sale', {
// 	// refresh: function(frm) {

// 	// }
// });

frappe.ui.form.on('Item on Sale', {
    offer_price: function(frm){
     
        frappe.call({
            method: 'done_with.services.rest.list_item',
            args: {
                "email": email
            },
            callback: function (r) {
                if (r.message) {
                    // Get the button element by its ID
    
                    // Add a click event listener to the button
                    offer_price.on("click", function() {
                        // Redirect to the offer price page
                        window.location.href = '/desk#List/Offer'; 
                    });
                }
            }
        });
    },
});
