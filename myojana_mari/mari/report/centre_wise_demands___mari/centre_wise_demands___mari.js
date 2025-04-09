// Copyright (c) 2024, suvaidyam and contributors
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
// if (frappe.user_roles.includes("Administrator")) {
// 	filters.push({
// 		"fieldname": "state",
// 		"fieldtype": "Link",
// 		"label": "State",
// 		"options": "State"
// 	},


// 	)
// }
frappe.query_reports["Centre wise demands - mari"] = {
	filters: filters,
};
