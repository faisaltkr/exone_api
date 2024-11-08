app_name = "exone_api"
app_title = "Exone Api"
app_publisher = "exone technologies"
app_description = "Api for mobiles and desktop apps"
app_email = "product@exonetechnologies.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/exone_api/css/exone_api.css"
# app_include_js = "/assets/exone_api/js/exone_api.js"

# include js, css files in header of web template
# web_include_css = "/assets/exone_api/css/exone_api.css"
# web_include_js = "/assets/exone_api/js/exone_api.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "exone_api/public/scss/website"

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
# app_include_icons = "exone_api/public/icons.svg"

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

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "exone_api.utils.jinja_methods",
# 	"filters": "exone_api.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "exone_api.install.before_install"
# after_install = "exone_api.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "exone_api.uninstall.before_uninstall"
# after_uninstall = "exone_api.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "exone_api.utils.before_app_install"
# after_app_install = "exone_api.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "exone_api.utils.before_app_uninstall"
# after_app_uninstall = "exone_api.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "exone_api.notifications.get_notification_config"

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

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    # "Sales Invoice": {
    #     "on_submit": "exone_api.api.save_sales_invoice"
		
    # }
	# "*": {
	# 	"on_update": "method",
	# 	"on_cancel": "method",
	# 	"on_trash": "method"
	# }
}




# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"exone_api.tasks.all"
# 	],
# 	"daily": [
# 		"exone_api.tasks.daily"
# 	],
# 	"hourly": [
# 		"exone_api.tasks.hourly"
# 	],
# 	"weekly": [
# 		"exone_api.tasks.weekly"
# 	],
# 	"monthly": [
# 		"exone_api.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "exone_api.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "exone_api.event.get_events"
# }

# override_whitelisted_methods = {
#     "frappe.core.doctype.user.user.login": "exone_api.api.login",
#     "frappe.desk.reportview.get_customers": "exone_api.api.get_customers",
#     "frappe.desk.reportview.get_items": "exone_api.api.get_items",
# }

# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "exone_api.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["exone_api.utils.before_request"]
# after_request = ["exone_api.utils.after_request"]

# Job Events
# ----------
# before_job = ["exone_api.utils.before_job"]
# after_job = ["exone_api.utils.after_job"]

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
# 	"exone_api.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

