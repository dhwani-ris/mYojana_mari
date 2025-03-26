// Copyright (c) 2023, suvaidyam and contributors
// For license information, please see license.txt

var filters = [
	{
		"fieldname": "from_date",
		"fieldtype": __("Date"),
		"label": "From Date",
	},
	{
		"fieldname": "to_date",
		"fieldtype": __("Date"),
		"label": "To Date"
	},
	{
		"fieldname": "state_of_origin",
		"fieldtype": "Link",
		"label": __("State"),
		"options":"State"
	},


];
// if (!frappe.user_roles.includes("MIS executive") || frappe.user_roles.includes("Administrator")) {
// 	filters.push({
// 		"fieldname": "centre",
// 		"fieldtype": "Link",
// 		"label": __("Centre"),
// 		"options": "Centre"
// 	})
// }
frappe.query_reports["Place of origin - mari"] = {
	filters: filters
};
