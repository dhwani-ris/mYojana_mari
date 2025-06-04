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
		{
			"fieldname": "district",
			"fieldtype": "Link",
			"label": __("District"),
			"options": "District",
			"get_query": function() {
				var state = frappe.query_report.get_filter_value('state');
				return {
					filters: {
						'state': state
					}
				};
			}
		},
		{
			"fieldname": "block",
			"fieldtype": "Link",
			"label": __("Cluster"),
			"options": "Block",
			"get_query": function() {
				var district = frappe.query_report.get_filter_value('district');
				return {
					filters: {
						'district': district
					}
				};
			},
		}
	)
}
frappe.query_reports["Milestone-wise demands - mari"] = {
	filters: filters,
};
