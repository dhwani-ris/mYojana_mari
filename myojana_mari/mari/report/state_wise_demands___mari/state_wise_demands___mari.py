# Copyright (c) 2023, suvaidyam and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from myojana.utils.report_filter import ReportFilter


def execute(filters=None):
    columns = [
        {
            "fieldname": "state_name",
            "label": _("Name Of State"),
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
    

    # condition_str = ReportFilter.set_report_filters(filters, 'follow_up_date', True , '_fuc')
    # condition_str = f"WHERE {condition_str}" if condition_str else ""
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
        select 
            COALESCE(ranked_followups.state_name, 'Unknown') AS state_name,
            SUM(CASE WHEN (ranked_followups.follow_up_status = 'Interested') THEN 1 ELSE 0 END) as open_demands,
            SUM(CASE WHEN (ranked_followups.follow_up_status = 'Completed') THEN 1 ELSE 0 END) as completed_demands, 
            SUM(CASE WHEN (ranked_followups.follow_up_status = 'Not interested' OR ranked_followups.follow_up_status = 'Not reachable') THEN 1 ELSE 0 END) as closed_demands, 
            SUM(CASE WHEN (ranked_followups.follow_up_status = 'Under process') THEN 1 ELSE 0 END) as submitted_demands, 
            SUM(CASE WHEN (ranked_followups.follow_up_status = 'Rejected') THEN 1 ELSE 0 END) as rejected_demands, 
            ( SUM(CASE WHEN (ranked_followups.follow_up_status = 'Interested') THEN 1 ELSE 0 END) + SUM(CASE WHEN (ranked_followups.follow_up_status = 'Completed') THEN 1 ELSE 0 END) + SUM(CASE WHEN (ranked_followups.follow_up_status = 'Not interested' OR ranked_followups.follow_up_status = 'Not reachable') THEN 1 ELSE 0 END) + SUM(CASE WHEN (ranked_followups.follow_up_status = 'Under process') THEN 1 ELSE 0 END) + SUM(CASE WHEN (ranked_followups.follow_up_status = 'Rejected') THEN 1 ELSE 0 END) ) as total_demands 
        from 
            ( 
                select 
                    _fuc.name_of_the_scheme,
                    _fuc.follow_up_status, 
                    _fuc.modified_by, 
                    s.state_name,
                    ROW_NUMBER() OVER (PARTITION BY  _fuc.parent,_fuc.name_of_the_scheme ORDER BY _fuc.modified DESC) as rn 
                from `tabFollow Up Child` as _fuc 
                INNER JOIN `tabBeneficiary Profiling` as ben_table 
                    ON (ben_table.name = _fuc.parent)
                LEFT JOIN
                    `tabState` s ON ben_table.state = s.name
                where 1=1
                    {condition_str}
            ) as ranked_followups 
        where ranked_followups.rn = 1 
        group by 
            COALESCE(ranked_followups.state_name, 'Unknown')
    """


    data = frappe.db.sql(sql_query, as_dict=True)
    return columns, data