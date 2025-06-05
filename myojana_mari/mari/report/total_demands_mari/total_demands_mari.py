import frappe
from myojana_mari.api import get_user_role_permission

def execute(filters=None):
	columns = [
		{
			"fieldname": "follow_up_status",
			"label": "Current status",
			"fieldtype": "Data",
			"width": 400,
		},
		{
			"fieldname": "count",
			"label": "Count",
			"fieldtype": "Int",
			"width": 400,
		},
	]
	user_perm = get_user_role_permission()

	state = user_perm.get('State')
	district = user_perm.get('District')
	block = user_perm.get('Block')
	slum = user_perm.get('Village')
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

	sql_query = f"""
		SELECT  
			CASE 
				WHEN fuc.follow_up_status = 'Interested' THEN 'Total Open Demand'
				WHEN fuc.follow_up_status IN ('Document submitted', 'Under process') THEN 'Total Submitted Demand'
				WHEN fuc.follow_up_status = 'Completed' THEN 'Total Completed Demand'
				WHEN fuc.follow_up_status = 'Not interested' THEN 'Total Close Demand'
				WHEN fuc.follow_up_status = 'Rejected' THEN 'Total Rejected Demand'
				ELSE fuc.follow_up_status
			END AS follow_up_status,
			COALESCE(COUNT(fuc.parent), 0) AS count
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
		WHERE fuc.rn = 1 AND fuc.follow_up_status != 'Not reachable'
		{condition_str}
		GROUP BY  
			CASE 
				WHEN fuc.follow_up_status = 'Interested' THEN 'Total Open Demand'
				WHEN fuc.follow_up_status IN ('Document submitted', 'Under process') THEN 'Total Submitted Demand'
				WHEN fuc.follow_up_status = 'Completed' THEN 'Total Completed Demand'
				WHEN fuc.follow_up_status = 'Not interested' THEN 'Total Close Demand'
				WHEN fuc.follow_up_status = 'Rejected' THEN 'Total Rejected Demand'
				ELSE fuc.follow_up_status
			END;
	"""

	data = frappe.db.sql(sql_query, as_dict=True)
	return columns, data
