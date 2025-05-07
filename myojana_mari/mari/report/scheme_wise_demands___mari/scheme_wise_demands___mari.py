# Copyright (c) 2023, suvaidyam and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from myojana.utils.report_filter import ReportFilter


def execute(filters=None):
    columns = [
        {
            "fieldname": "user",
            "label": _("User Name"),
            "fieldtype": "Data",
            "width": 150,

        },
        {
            "fieldname": "milestone",
            "label": _("Milestone category"),
            "fieldtype": "Data",
            "width": 150,

        },
        {
            "fieldname": "scheme",
            "label": _("Scheme"),
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
        },
    ]
    user = frappe.session.user
    condition_str = ReportFilter.set_report_filters(filters, 'follow_up_date', True , '_fuc')
    if condition_str:
        condition_str = f"AND {condition_str}"
    else:
        condition_str = ""
    # check user role
    if 'Sub-Centre' in frappe.get_roles(user) and 'Administrator' not in frappe.get_roles(user):
        condition_str += f" AND _fuc.modified_by = '{user}'"
    sql_query = f"""
        select 
            ranked_followups.name_of_the_scheme AS scheme,
            ranked_followups.milestone AS milestone,
            ranked_followups.modified_by AS user,
            SUM(CASE WHEN (ranked_followups.follow_up_status = 'Interested') THEN 1 ELSE 0 END) as open_demands,
            SUM(CASE WHEN (ranked_followups.follow_up_status = 'Completed') THEN 1 ELSE 0 END) as completed_demands,
            SUM(CASE WHEN (ranked_followups.follow_up_status = 'Closed') THEN 1 ELSE 0 END) as closed_demands,
            SUM(CASE WHEN (ranked_followups.follow_up_status = 'Under process') THEN 1 ELSE 0 END) as submitted_demands,
            SUM(CASE WHEN (ranked_followups.follow_up_status = 'Rejected') THEN 1 ELSE 0 END) as rejected_demands,
            (
                SUM(CASE WHEN (ranked_followups.follow_up_status = 'Interested') THEN 1 ELSE 0 END) +
                SUM(CASE WHEN (ranked_followups.follow_up_status = 'Completed') THEN 1 ELSE 0 END) +
                SUM(CASE WHEN (ranked_followups.follow_up_status = 'Closed') THEN 1 ELSE 0 END) +
                SUM(CASE WHEN (ranked_followups.follow_up_status = 'Under process') THEN 1 ELSE 0 END) +
                SUM(CASE WHEN (ranked_followups.follow_up_status = 'Rejected') THEN 1 ELSE 0 END)
            ) as total_demands
        from (
            select  
                _fuc.name_of_the_scheme,
                _sc.milestone,
                _fuc.follow_up_status,
                _fuc.modified_by,
                ROW_NUMBER() OVER (PARTITION BY _fuc.parent,_fuc.name_of_the_scheme ORDER BY _fuc.modified DESC) as rn
            from
                `tabFollow Up Child` as _fuc
            INNER JOIN `tabScheme` AS _sc ON (_sc.name = _fuc.name_of_the_scheme)
            WHERE
                1=1 
                {condition_str}
        ) as ranked_followups
        where ranked_followups.rn = 1 
        group by 
            ranked_followups.name_of_the_scheme,
            ranked_followups.milestone,
            ranked_followups.modified_by
    """
    data = frappe.db.sql(sql_query, as_dict=True)
    return columns, data
