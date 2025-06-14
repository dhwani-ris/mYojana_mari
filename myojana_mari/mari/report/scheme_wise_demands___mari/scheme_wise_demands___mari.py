# Copyright (c) 2023, suvaidyam and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from myojana.utils.report_filter import ReportFilter
from myojana_mari.api import get_user_role_permission


def execute(filters=None):
    columns = [
        # {
        #     "fieldname": "user",
        #     "label": _("User Name"),
        #     "fieldtype": "Data",
        #     "width": 150,

        # },
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
            "width": 170,
        },
        {
            "fieldname": "closed_demands",
            "label": _("Closed Demands"),
            "fieldtype": "Data",
            "width": 170,
        },
    ]
    user_perm = get_user_role_permission()
    state = user_perm.get('State')
    district = user_perm.get('District')
    block = user_perm.get('Block')
    slum = user_perm.get('Village')
    user = frappe.session.user
    # condition_str = ReportFilter.set_report_filters(filters, 'follow_up_date', True , 'fuc')
    # if condition_str:
    #     condition_str = f"AND {condition_str}"
    # else:
    #     condition_str = ""
    condition_str = ""
    if filters.get("from_date") and filters.get("to_date"):
        condition_str += f" AND fuc.follow_up_date BETWEEN '{filters.get('from_date')}' AND '{filters.get('to_date')}'"
    elif filters.get("from_date"):
        condition_str += f" AND fuc.follow_up_date >= '{filters.get('from_date')}'"
    elif filters.get("to_date"):
        condition_str += f" AND fuc.follow_up_date <= '{filters.get('to_date')}'"

    # Handle state filter with multiple permissions
    if state:
        if isinstance(state, list):
            state_list = "', '".join(state)
            condition_str += f" AND ben.state IN ('{state_list}')"
        else:
            condition_str += f" AND ben.state = '{state}'"

    # Handle district filter with multiple permissions
    if district:
        if isinstance(district, list):
            district_list = "', '".join(district)
            condition_str += f" AND ben.district IN ('{district_list}')"
        else:
            condition_str += f" AND ben.district = '{district}'"

    # Handle block filter with multiple permissions
    if block:
        if isinstance(block, list):
            block_list = "', '".join(block)
            condition_str += f" AND ben.ward IN ('{block_list}')"
        else:
            condition_str += f" AND ben.ward = '{block}'"

    # Handle village/slum filter with multiple permissions
    if slum:
        if isinstance(slum, list):
            slum_list = "', '".join(slum)
            condition_str += f" AND ben.name_of_the_settlement IN ('{slum_list}')"
        else:
            condition_str += f" AND ben.name_of_the_settlement = '{slum}'"

    # check user role
    # if 'Sub-Centre' in frappe.get_roles(user) and 'Administrator' not in frappe.get_roles(user):
    #     condition_str += f" AND fuc.last_update_by = '{user}'"
    elif filters.get('modified_by'):
        condition_str += f" AND fuc.last_update_by = '{filters.get('modified_by')}'"
    sql_query = f"""
        SELECT
            ranked.name_of_the_scheme,
            ranked.milestone,
            SUM(CASE WHEN (ranked.follow_up_status = 'Interested') THEN 1 ELSE 0 END) as open_demands,
            SUM(CASE WHEN (ranked.follow_up_status = 'Completed') THEN 1 ELSE 0 END) as completed_demands, 
            SUM(CASE WHEN (ranked.follow_up_status = 'Not interested') THEN 1 ELSE 0 END) as closed_demands, 
            SUM(CASE WHEN (ranked.follow_up_status = 'Under process' OR ranked.follow_up_status = 'Document submitted' OR ranked.follow_up_status = 'Additional info required') THEN 1 ELSE 0 END) as submitted_demands, 
            SUM(CASE WHEN (ranked.follow_up_status = 'Rejected') THEN 1 ELSE 0 END) as rejected_demands, 
            ( SUM(CASE WHEN (ranked.follow_up_status = 'Interested') THEN 1 ELSE 0 END) + SUM(CASE WHEN (ranked.follow_up_status = 'Completed') THEN 1 ELSE 0 END) + SUM(CASE WHEN (ranked.follow_up_status = 'Not interested') THEN 1 ELSE 0 END) + SUM(CASE WHEN (ranked.follow_up_status = 'Under process' OR ranked.follow_up_status = 'Document submitted' OR ranked.follow_up_status = 'Additional info required') THEN 1 ELSE 0 END) + SUM(CASE WHEN (ranked.follow_up_status = 'Rejected') THEN 1 ELSE 0 END)) as total_demands

        FROM (
            SELECT 
                fuc.name_of_the_scheme,
                fuc.follow_up_status,
                fuc.last_update_by,
                fuc.follow_up_date,
                fuc.parent,
                sch.milestone,
                ben.state,
                ben.district,
                ben.ward
            FROM (
                SELECT *,
                    ROW_NUMBER() OVER (
                        PARTITION BY parent, name_of_the_scheme
                        ORDER BY last_update_date DESC
                    ) AS rn
                FROM "tabFollow Up Child"
            ) fuc
            JOIN "tabBeneficiary Profiling" ben ON ben.name = fuc.parent
            JOIN "tabScheme" sch ON sch.name = fuc.name_of_the_scheme
            WHERE fuc.rn = 1 {condition_str}
        ) ranked
        GROUP BY 
            ranked.name_of_the_scheme,
            ranked.milestone
        
        ORDER BY 
            ranked.name_of_the_scheme, ranked.milestone;
    """
    data = frappe.db.sql(sql_query, as_dict=True)
    return columns, data
