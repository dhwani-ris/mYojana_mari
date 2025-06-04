// Copyright (c) 2024, suvaidyam and contributors
// For license information, please see license.txt
var filters = [
	{
		"fieldname": "from_date",
		"fieldtype": "Date",
		"label": __("From Date"),
	},
	{
		"fieldname": "to_date",
		"fieldtype": "Date",
		"label": __("To Date")
	},


];
if(frappe.user_roles.some(role => ['MIS executive','CSC Member','Admin','Administrator'].includes(role))){
	filters.push(
		{
			"fieldname": "state",
			"fieldtype": "Link",
			"label": __("State"),
			"options": "State",
		},
	)
}
frappe.query_reports["State-wise demands - mari"] = {
	filters: filters,
};
