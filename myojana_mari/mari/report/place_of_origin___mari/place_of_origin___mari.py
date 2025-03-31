# Copyright (c) 2023, suvaidyam and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from myojana.utils.report_filter import ReportFilter


def execute(filters=None):
    columns = [
        {
            "fieldname": "state",
            "label": _("State of Origin"),
            "fieldtype": "Data",
            "width": 200
        },
        {
            "fieldname": "district",
            "label": _("District of Origin"),
            "fieldtype": "Data",
            "width": 200
        },
        {
            "fieldname": "block",
            "label": _("Cluster"),
            "fieldtype": "Data",
            "width": 200
        },
        {
            "fieldname": "count",
            "label": _("Count"),
            "fieldtype": "int",
            "width": 200
        }
    ]
    condition_str = ReportFilter.set_report_filters(filters, 'date_of_visit', True, 'b')
    if condition_str:
        condition_str = f"{condition_str}"
    else:
        condition_str = "1=1"

    sql_query = f"""
    SELECT
        COALESCE(NULLIF(s.state_name, ''), 'Unknown') AS state,
        COALESCE(NULLIF(d.district_name, ''), 'Unknown') AS district,
        COALESCE(NULLIF(bl.block_name, ''), 'Unknown') AS block,
        COUNT(b.name) AS count
    FROM
        `tabBeneficiary Profiling` AS b
        LEFT JOIN `tabState` AS s ON b.state_of_origin = s.name
        LEFT JOIN `tabDistrict` AS d ON b.district_of_origin = d.name
        LEFT JOIN `tabBlock` as bl ON b.ward = bl.name
    WHERE {condition_str}
    GROUP BY
        COALESCE(NULLIF(s.state_name, ''), 'Unknown'), 
        COALESCE(NULLIF(d.district_name, ''), 'Unknown'), 
        COALESCE(NULLIF(bl.block_name, ''), 'Unknown')
    ORDER BY
        COALESCE(NULLIF(s.state_name, ''), 'Unknown'), 
        COALESCE(NULLIF(d.district_name, ''), 'Unknown');

    """
    data = frappe.db.sql(sql_query, as_dict=True, debug=True)
    frappe.db.rollback()

    return columns, data
