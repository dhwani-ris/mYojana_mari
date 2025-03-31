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
	}
	
];
if (frappe.user_roles.includes("Administrator")) {
	filters.push({
		"fieldname": "state",
		"fieldtype": "Link",
		"label": "State",
		"options": __("State")
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
	}
	)
}
frappe.query_reports["Religion-wise beneficiaries - mari"] = {
	filters: filters
};
