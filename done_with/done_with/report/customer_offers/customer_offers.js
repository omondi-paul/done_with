// Copyright (c) 2024, Polito and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Customer Offers"] = {
	"filters": [
		{
			"fieldname" : "customer_name",
			"labels": __('Customer Name'),
			"fieldtype": 'Link',
			"options": "Listing Request",
			"width": 100,
			"reqd": 0

		}

	]

};
