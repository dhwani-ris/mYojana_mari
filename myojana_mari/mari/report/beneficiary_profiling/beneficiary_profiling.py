# Copyright (c) 2023, suvaidyam and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from myojana.utils.report_filter import ReportFilter


def execute(filters=None):
    columns = [
        {
            "fieldname": "ben_id",
            "label": _("ID"),
            "fieldtype": "Data",
            "width": 100,

        },
        {
            "fieldname": "name_of_the_beneficiary",
            "label": _("Full Name"),
            "fieldtype": "Data",
            "width": 200,

        },
        {
            "fieldname": "custom_custon_contact_number",
            "label": _("Contact Number"),
            "fieldtype": "Data",
            "width": 200,

        },
        {
            "fieldname": "name_of_the_scheme",
			"label": _("Scheme Name"),
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "state_name",
			"label": _("State"),
            "fieldtype": "Data",
            "width": 130,
        },
        {
            "fieldname": "district_name",
			"label": _("District"),
            "fieldtype": "Data",
            "width": 160,
        },
        {
            "fieldname": "block_name",
			"label": _("Block"),
            "fieldtype": "Data",
            "width": 170,
        },
        {
            "fieldname": "milestone",
			"label": _("Milestone"),
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "follow_up_status",
			"label": _("Follow Up Status"),
            "fieldtype": "Data",
            "width": 130,
        }
    ]

    # condition_str = ReportFilter.set_report_filters(filters, 'follow_up_date', True , 'fuc')
    # condition_str = f"WHERE {condition_str}" if condition_str else ""
    condition_str = ""
    if filters.get("from_date") and filters.get("to_date"):
        condition_str += f" AND fuc.follow_up_date BETWEEN '{filters.get('from_date')}' AND '{filters.get('to_date')}'"
    elif filters.get("from_date"):
        condition_str += f" AND fuc.follow_up_date >= '{filters.get('from_date')}'"
    elif filters.get("to_date"):
        condition_str += f" AND fuc.follow_up_date <= '{filters.get('to_date')}'"
    if filters.get('state'):
        condition_str += f" AND ben.state = '{filters.get('state')}'"
    if filters.get('district'):
        condition_str += f" AND ben.district = '{filters.get('district')}'"
    if filters.get('block'):
        condition_str += f" AND ben.block = '{filters.get('block')}'"
    if filters.get('status'):
        condition_str += f" AND fuc.follow_up_status = '{filters.get('status')}'"
    sql_query = f"""
            SELECT
				ranked.ben_id,
				ranked.name_of_the_beneficiary,
				ranked.custom_custon_contact_number,
				ranked.state_name,
				ranked.district_name,
				ranked.block_name,
				ranked.name_of_the_scheme,
				ranked.milestone,
				ranked.last_update_by,
				ranked.follow_up_status
			FROM (
				SELECT 
					fuc.name_of_the_scheme,
					fuc.follow_up_status,
					fuc.last_update_by,
					fuc.parent,
					sch.milestone,
					ben.name_of_the_beneficiary,
					ben.custom_custon_contact_number,
					ben.state,
					st.state_name,
					ben.district,
					dt.district_name,
					ben.ward,
					bl.block_name,
					ben.name as ben_id
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
				LEFT JOIN `tabState` st ON ben.state = st.name
				LEFT JOIN `tabDistrict` dt ON ben.district = dt.name
				LEFT JOIN `tabBlock` bl ON ben.ward = bl.name
				WHERE fuc.rn = 1 {condition_str}
			) ranked
        """


    data = frappe.db.sql(sql_query, as_dict=True)
    return columns, data