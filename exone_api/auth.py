# Copyright (c) 2023, Wahni IT Solutions and contributors
# For license information, please see license.txt

import base64
import json

import frappe
from frappe.utils.password import get_decrypted_password
from frappe.utils.password import update_password
from frappe.utils.password_strength import test_password_strength
from frappe.core.doctype.user.user import reset_password


@frappe.whitelist(allow_guest=True)
def authenticate():
	try:
		data = json.loads(frappe.request.data)
		username = data.get("username")
		password = data.get("password")

		try:
			login_manager = frappe.auth.LoginManager()
			login_manager.authenticate(user=username, pwd=password)
		except Exception:
			frappe.local.response["status_code"] = 400
			return {"success": False, "message": "Invalid username or password"}

		login_manager.post_login()
		user = frappe.session.user
		user_details = frappe.db.get_value(
			"User", user, 
			["email", "first_name", "last_name", "full_name", "mobile_no", "user_type", "enabled"], as_dict=True
		)

		applicable_pos_profiles = frappe.db.get_all(
            'POS Profile User',
            filters={'user': user},
            fields=['parent']
        )

        # If there are no applicable POS profiles, return an empty list
		if not applicable_pos_profiles:
			return {
                'pos_profiles': []
            }

        # Extract the POS profile names
		pos_profile_names = [profile['parent'] for profile in applicable_pos_profiles]	
		pos_profiles = frappe.db.get_all(
            'POS Profile',
            filters={'name': ['in', pos_profile_names]},
            fields=['name', 'company', 'currency', 'warehouse', 'cost_center', 'write_off_account'],
            order_by='name'
        )
		for profile in pos_profiles:
            # Fetch Applicable Users for each POS Profile
			profile['applicable_users'] = frappe.db.get_all(
                'POS Profile User',
                filters={'parent': profile['name']},
                fields=['user']
            )

            # Fetch Payment Methods for each POS Profile
			profile['payment_methods'] = frappe.db.get_all(
                'POS Payment Method',
                filters={'parent': profile['name']},
                fields=['mode_of_payment']
            )
		return {
			"success": True,
			"message": "Logged in succesfully",
			"token": generate_keys(username),
			'user_details':user_details,
			"pos_profile_details":pos_profiles
		}
	except Exception as e:
		frappe.log_error(str(e), "Auth Error")
		return {"success": False, "error": str(e)}


def generate_keys(user):
	api_secret = get_decrypted_password("User", user, "api_secret", raise_exception=False)
	if not api_secret:
		user_details = frappe.get_doc("User", user)
		api_secret = frappe.generate_hash(length=15)
		# if api key is not set generate api key
		if not user_details.api_key:
			api_key = frappe.generate_hash(length=15)
			user_details.api_key = api_key
		user_details.api_secret = api_secret
		user_details.save()
	else:
		api_key = frappe.db.get_value("User", user, "api_key")

	return base64.b64encode(('{}:{}'.format(api_key, api_secret)).encode('utf-8')).decode('utf-8')


@frappe.whitelist()
def change_password():
	try:
		data = json.loads(frappe.request.data)			
		new_password = data.get("new_password")
		old_password = data.get("old_password")
		
		if new_password == old_password:
			return {"success": False, "message": "New password must be different from the old password."}

		try:
			frappe.local.login_manager.check_password(frappe.session.user, old_password)
		except:
			return {"success": False, "message": "Wrong password"}

		user_data = frappe.db.get_value(
			"User", frappe.session.user, ["first_name", "middle_name", "last_name", "email", "birth_date"]
		)

		result = test_password_strength(new_password, user_inputs=user_data)
		feedback = result.get("feedback", {})

		if feedback and not feedback.get("password_policy_validation_passed", False):
			return {"success": False, "message": "Password does not meet the requirements", **feedback}


		update_password(user=frappe.session.user, pwd=new_password, doctype="User", fieldname="password", logout_all_sessions=True)
		
		return {"success": True, "message": "Password Changed", **feedback}

	except Exception as e:
		frappe.log_error(message=str(frappe.get_traceback()), title="Password Change Error")
		return {"success": False, "message": str(e)}


@frappe.whitelist(allow_guest=True)
def forgot_password():
	try:
		data = json.loads(frappe.request.data)
		reset_password(data.get("user"))
		return {"success": True, "message": "Password reset instructions have been sent to your email."}
	except Exception as e:
		frappe.log_error(message=str(frappe.get_traceback()), title="Forgot Password Error")
		return {"success": False, "message": str(e)}
