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


];
if(frappe.user_roles.some(role => ['MIS executive','CSC Member','Admin','Administrator'].includes(role))){
	filters.push(
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
		}
	)
}
frappe.query_reports["Cluster Wise Demands"] = {
	filters: filters,
};
