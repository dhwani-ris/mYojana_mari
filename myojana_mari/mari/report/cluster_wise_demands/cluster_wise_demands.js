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

];
frappe.query_reports["Cluster Wise Demands"] = {
	filters: filters,
};
