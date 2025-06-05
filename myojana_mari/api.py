import frappe
from frappe import _

def get_user_role_permission():
    user = frappe.session.user
    user_permissions = frappe.get_list('User Permission', filters={
                                       "user": user}, fields=['allow', 'for_value'],ignore_permissions=True)
    result = {}
    
    for item in user_permissions:
        if item["allow"] not in result:
            result[item["allow"]] = []
        result[item["allow"]].append(item["for_value"])
    
    # Convert single item lists to single values for backward compatibility
    for key in result:
        if len(result[key]) == 1:
            result[key] = result[key][0]
            
    return result