# Copyright (c) 2022, Wahni IT Solutions and contributors
# For license information, please see license.txt

import json
import frappe
from frappe import _


@frappe.whitelist()
# def fetch_customers():
# 	try:
# 		return {"success": True, "customers": frappe.get_all('Customer',fields=['name', 'customer_name', 'customer_group', 'territory', 'customer_type'])}
# 	except Exception as e:
# 		return {"success": False, "message": str(e)}

def get_customers():
    # Fetch customer details
    customers = frappe.db.get_all('Customer', fields=['name','tax_id','custom_b2c', 'customer_group', 'territory', 'customer_type'])

    # Fetch addresses linked to each customer
    for customer in customers:
        customer['addresses'] = frappe.db.get_all(
            'Address', 
            filters={'link_name': customer['name'], 'link_doctype': 'Customer'}, 
            fields=['address_line1', 'address_line2', 'city', 'state', 'country', 'pincode']
        )

    return customers


@frappe.whitelist()
def create_customer():
	try:
		data = json.loads(frappe.request.data)
		customer = frappe.new_doc("Customer")

		for key, value in data.items():
			customer.set(key, value)

		customer.insert(ignore_permissions=True, ignore_mandatory=True)
		return {"success": True, "message": "Customer Created"}
	except Exception as e:
		frappe.log_error(str(frappe.get_traceback()), "Customer Creation Error")
		return {"success": False, "message": str(e)}


@frappe.whitelist()
def fetch_customer_groups():
	try:
		return {"success": True, "customer_groups": frappe.get_list('Customer Group')}
	except Exception as e:
		return {"success": False, "message": str(e)}


@frappe.whitelist()
def fetch_item_groups():
	try:
		return {"success": True, "item_groups": frappe.get_list('Item Group')}
	except Exception as e:
		return {"success": False, "message": str(e)}


# @frappe.whitelist()
# def fetch_items():
# 	try:
# 		return {"success": True, "items": frappe.get_list('Item', fields=['name', 'item_name', 'item_group', 'stock_uom', 'sales_uom'])}
# 	except Exception as e:
# 		return {"success": False, "message": str(e)}

@frappe.whitelist()
def get_items_with_tax_template():
    try:
        # Fetch item details, including the 'item_tax_template' field
        items = frappe.get_all('Item', 
                               fields=['item_code', 'item_name', 'description', 'standard_rate', 'stock_uom', 'is_stock_item','image','item_name_arabic'])

        for item in items:

            	item['tax_details'] = frappe.get_all(
                    'Item Tax', 
                    filters={'parent': item['item_code']}, 
                    fields=['item_tax_template']
                )
                # Fetch tax details from the Item Tax Template linked to this item
                #tax_template_name = item['tax_details'][0]['item_tax_template']

                # item['tax_details']= frappe.get_all(
                #     'Item Tax Template', 
                #     filters={'parent': tax_template_name}, 
                #     fields=['tax_type', 'tax_rate']
                # )
            

        return {
            'items': items
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Failed to fetch Items with Tax Template"))
        frappe.throw(_("An error occurred while fetching Items with Tax Template"))

# @frappe.whitelist()
# def get_pos_profile_and_printer_configs():
#     # Fetch POS Profiles along with Applicable Users and Payment Methods
#     pos_profiles = frappe.db.get_all('POS Profile', 
#                                      fields=['name', 'company', 'currency', 'warehouse', 'cost_center', 'write_off_account'],
#                                      order_by='name')

#     for profile in pos_profiles:
#         # Fetch Applicable Users for each POS Profile
#         profile['applicable_users'] = frappe.db.get_all(
#             'POS Profile User',
#             filters={'parent': profile['name']},
#             fields=['user']
#         )

#         # Fetch Payment Methods for each POS Profile
#         profile['payment_methods'] = frappe.db.get_all(
#             'POS Payment Method',
#             filters={'parent': profile['name']},
#             fields=['mode_of_payment']
#         )

#     # Fetch Printer Configurations
#     # printer_configs = frappe.db.get_all('Printer Settings', fields=['name', 'printer_ip', 'default_printer', 'printer_name', 'enabled'])

#     return {
#         'pos_profiles': pos_profiles,
    
#     }


@frappe.whitelist()
def get_pos_profile_and_printer_configs(user):
    try:
        # Find POS Profiles where the given user is listed in the "POS Profile User" child table
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

        # Fetch POS Profiles that match the filtered names
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

            #     # Fetch Printer Configurations

        return {
            'pos_profiles': pos_profiles,
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Failed to fetch POS Profiles and Printer Configurations"))
        frappe.throw(_("An error occurred while fetching POS Profiles and Printer Configurations"))
