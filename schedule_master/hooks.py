# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "schedule_master"
app_title = "Schedule Master"
app_publisher = "Hardik Gadesha"
app_description = "App for Payment Reminder"
app_icon = "octicon octicon-file-directory"
app_color = "lightcoral"
app_email = "hardikgadesha@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/schedule_master/css/schedule_master.css"
# app_include_js = "/assets/schedule_master/js/schedule_master.js"

# include js, css files in header of web template
# web_include_css = "/assets/schedule_master/css/schedule_master.css"
# web_include_js = "/assets/schedule_master/js/schedule_master.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "schedule_master.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "schedule_master.install.before_install"
# after_install = "schedule_master.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

notification_config = "schedule_master.notifications.get_notification_config"

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
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
	"cron": {
                "0 17 * * *": [
                        "schedule_master.schedule_master.overdue.send_draft"
                ],
		"0 8 * * Thu": [
                        "schedule_master.schedule_master.overdue.sendmail"
                ]
        }
}

# Testing
# -------

# before_tests = "schedule_master.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "schedule_master.event.get_events"
# }

