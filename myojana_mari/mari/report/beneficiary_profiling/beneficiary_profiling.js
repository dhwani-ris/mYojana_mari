// Copyright (c) 2025, Rahul Sah and contributors
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
			return {
				filters: {
					"state": frappe.query_report.get_filter_value("state")
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
			return {
				filters: {
					"district": frappe.query_report.get_filter_value("district")
				}
			};
		}
	},
	{
		"fieldname": "village",
		"fieldtype": "Link",
		"label": "Slum",
		"options": "Village",
		"get_query": function() {
			return {
				filters: {
					"block": frappe.query_report.get_filter_value("block")
				}
			};
		}
	},
	{
		"fieldname":'status',
		"fieldtype": "Select",
		"label": "Status",
		"options": "\nInterested\nNot interested\nDocument submitted\nRejected\nNot reachable\nCompleted\nUnder process\nAdditional info required",
	}

];
frappe.query_reports["Beneficiary Profiling"] = {
	filters: filters,
};
