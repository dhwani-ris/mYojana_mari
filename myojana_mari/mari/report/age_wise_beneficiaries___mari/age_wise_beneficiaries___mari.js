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
		"fieldtype": "Date",
		"label": __("To Date")
	},
];
if (frappe.user_roles.includes("Admin")) {
	filters.push(
		{
			"fieldname": "centre",
			"fieldtype": "Link",
			"label": __("Centre"),
			"options": "Centre"
		},
		{
			"fieldname": "district",
			"fieldtype": "Link",
			"label": __("District"),
			"options": "District",
			"get_query": function () {
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
frappe.query_reports["Age-wise beneficiaries - mari"] = {
	filters: filters
};



