// Copyright (c) 2023, suvaidyam and contributors
// For license information, please see license.txt
var filters = [
	{
		"fieldname": "from_date",
		"fieldtype": "Date",
		"label": "From Date",
	},
	{
		"fieldname": "to_date",
		"fieldtype": "Date",
		"label": "To Date"
	},
	{
		"fieldname": "state",
		"fieldtype": "Link",
		"label": "State",
		"options": "State"
	},
	{
		"fieldname": "district",
		"fieldtype": "Link",
		"label": "District",
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
		"label": "Cluster",
		"options": "Block",
		"get_query": function() {
			var district = frappe.query_report.get_filter_value('district');
			return {
				filters: {
					'district': district
				}
			};
		}
	},
	
];

frappe.query_reports["House type-wise beneficiaries - mari"] = {
	filters: filters
};
