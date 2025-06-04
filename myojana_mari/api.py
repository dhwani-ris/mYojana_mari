import frappe
from frappe import _

def get_user_role_permission():
    user = frappe.session.user
    user_permissions = frappe.get_list('User Permission', filters={
                                       "user": user}, fields=['allow', 'for_value'],ignore_permissions=True)
    result = {}
    for item in user_permissions:
        result[item["allow"]] = item["for_value"]
    return result