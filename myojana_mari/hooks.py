app_name = "myojana_mari"
app_title = "Mari"
app_publisher = "Rahul Sah"
app_description = "Mari"
app_email = "rahul.sah@dhwaniris.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

fixtures = [
    # "mYojana Settings",
    # "Report List",
    # "SVA Report"
    # "scheme application submitted",
    # "Scheme Paid by",
    # "Client Script",
    # "Custom HTML Block",
    # "Custom Field"

]
# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "myojana_mari",
# 		"logo": "/assets/myojana_mari/logo.png",
# 		"title": "Mari",
# 		"route": "/myojana_mari",
# 		"has_permission": "myojana_mari.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/myojana_mari/css/myojana_mari.css"
# app_include_js = "/assets/myojana_mari/js/myojana_mari.js"

# include js, css files in header of web template
# web_include_css = "/assets/myojana_mari/css/myojana_mari.css"
# web_include_js = "/assets/myojana_mari/js/myojana_mari.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "myojana_mari/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "myojana_mari/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "myojana_mari.utils.jinja_methods",
# 	"filters": "myojana_mari.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "myojana_mari.install.before_install"
# after_install = "myojana_mari.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "myojana_mari.uninstall.before_uninstall"
# after_uninstall = "myojana_mari.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "myojana_mari.utils.before_app_install"
# after_app_install = "myojana_mari.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "myojana_mari.utils.before_app_uninstall"
# after_app_uninstall = "myojana_mari.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "myojana_mari.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"myojana_mari.tasks.all"
# 	],
# 	"daily": [
# 		"myojana_mari.tasks.daily"
# 	],
# 	"hourly": [
# 		"myojana_mari.tasks.hourly"
# 	],
# 	"weekly": [
# 		"myojana_mari.tasks.weekly"
# 	],
# 	"monthly": [
# 		"myojana_mari.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "myojana_mari.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "myojana_mari.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "myojana_mari.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["myojana_mari.utils.before_request"]
# after_request = ["myojana_mari.utils.after_request"]

# Job Events
# ----------
# before_job = ["myojana_mari.utils.before_job"]
# after_job = ["myojana_mari.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"myojana_mari.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

