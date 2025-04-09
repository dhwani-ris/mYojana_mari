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
		"label": __("State of Origin"),
		"options": "State",
	},
	{
		"fieldname": "district_of_origin",
		"fieldtype": "Link",
		"label": __("District of Origin"),
		"options": "District",
		"get_query": function() {
			var state = frappe.query_report.get_filter_value('state_of_origin');
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
			var district = frappe.query_report.get_filter_value('district_of_origin');
			return {
				filters: {
					'district': district
				}
			};
		},
	}


];

frappe.query_reports["Place of origin - mari"] = {
	filters: filters
};
