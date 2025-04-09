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
	{
		"fieldname": "state",
		"fieldtype": "Link",
		"label": __("State"),
		"options": "State"
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
		}
	}
	
];

frappe.query_reports["District-wise demands - mari"] = {
	filters: filters,
};
