# Copyright (c) 2023, suvaidyam and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from myojana.utils.report_filter import ReportFilter


def execute(filters=None):
    columns = [
        {
            "fieldname": "user",
            "label": _("User"),
            "fieldtype": "Data",
            "width": 200,

        },
        {
            "fieldname": "sub_centre_name",
            "label": _("Sub Centre Name"),
            "fieldtype": "Data",
            "width": 200,

        },
        {
            "fieldname": "total_demands",
            "label": _("Total Demands"),
            "fieldtype": "Data",
            "width": 130,
        },
        {
            "fieldname": "open_demands",
            "label": _("Open Demands"),
            "fieldtype": "Data",
            "width": 130,
        },
        {
            "fieldname": "submitted_demands",
            "label": _("Submitted Demands"),
            "fieldtype": "Data",
            "width": 160,
        },
        {
            "fieldname": "completed_demands",
            "label": _("Completed Demands"),
            "fieldtype": "Data",
            "width": 170,
        },
        {
            "fieldname": "rejected_demands",
            "label": _("Rejected Demands"),
            "fieldtype": "Data",
            "width": 130,
        },
        {
            "fieldname": "closed_demands",
            "label": _("Closed Demands"),
            "fieldtype": "Data",
            "width": 130,
        }
    ]             
    

    # condition_str = ReportFilter.set_report_filters(filters, 'follow_up_date', True , '_fuc')
    # condition_str = f"{condition_str}" if condition_str else "1=1"
    condition_str = ""
    if filters.get("from_date") and filters.get("to_date"):
        condition_str += f" AND _fuc.follow_up_date BETWEEN '{filters.get('from_date')}' AND '{filters.get('to_date')}'"
    elif filters.get("from_date"):
        condition_str += f" AND _fuc.follow_up_date >= '{filters.get('from_date')}'"
    elif filters.get("to_date"):
        condition_str += f" AND _fuc.follow_up_date <= '{filters.get('to_date')}'"
    if filters.get('state'):
        condition_str += f" AND ben_table.state = '{filters.get('state')}'"

    sql_query = f"""
    SELECT
        _sc.modified_by AS user,
        COALESCE(hd.sub_centre_name, 'Unknown') AS sub_centre_name,
        SUM(CASE WHEN _sc.status = 'Open' THEN 1 ELSE 0 END) AS open_demands,
        SUM(CASE WHEN _sc.status = 'Completed' THEN 1 ELSE 0 END) AS completed_demands,
        SUM(CASE WHEN _sc.status = 'Closed' THEN 1 ELSE 0 END) AS closed_demands,
        SUM(CASE WHEN _sc.status = 'Under process' THEN 1 ELSE 0 END) AS submitted_demands,
        SUM(CASE WHEN _sc.status = 'Rejected' THEN 1 ELSE 0 END) AS rejected_demands,
        COUNT(_sc.status) AS total_demands
    FROM
        `tabScheme Child` as _sc
	LEFT JOIN `tabFollow Up Child` as _fuc
		ON (_fuc.name_of_the_scheme = _sc.name_of_the_scheme AND _fuc.parenttype = 'Beneficiary Profiling')
	INNER JOIN `tabBeneficiary Profiling` as ben_table 
		ON (ben_table.name = _sc.parent)
    LEFT JOIN
        "tabSub Centre" hd ON ben_table.sub_centre = hd.name 
    WHERE 1=1
        {condition_str}
    GROUP BY
        _sc.modified_by, COALESCE(hd.sub_centre_name, 'Unknown');


    """



    data = frappe.db.sql(sql_query, as_dict=True)
    return columns, data