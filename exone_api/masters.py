# Copyright (c) 2022, Wahni IT Solutions and contributors
# For license information, please see license.txt

import json
import frappe
from frappe import _



# def fetch_customers():
# 	try:
# 		return {"success": True, "customers": frappe.get_all('Customer',fields=['name', 'customer_name', 'customer_group', 'territory', 'customer_type'])}
# 	except Exception as e:
# 		return {"success": False, "message": str(e)}
@frappe.whitelist(allow_guest=False)
def get_customers():
    # Fetch customer details
    customers = frappe.db.get_all('Customer', fields=['name','tax_id','custom_b2c', 'customer_group', 'territory', 'customer_type','naming_series','customer_name'])

    # Fetch addresses linked to each customer
    for customer in customers:
        customer['addresses'] = frappe.db.get_all(
            'Address', 
            filters={'link_name': customer['name'], 'link_doctype': 'Customer'}, 
            fields=['address_line1', 'address_line2', 'city', 'state', 'country', 'pincode']
        )

    return customers


@frappe.whitelist(allow_guest=False)
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


@frappe.whitelist(allow_guest=False)
def fetch_customer_groups():
	try:
		return {"success": True, "customer_groups": frappe.get_list('Customer Group')}
	except Exception as e:
		return {"success": False, "message": str(e)}


@frappe.whitelist(allow_guest=False)
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

@frappe.whitelist(allow_guest=False)
def get_items_with_tax_template():
	try:
        # Fetch item details, including the 'item_tax_template' field
		items = frappe.get_all('Item', 
                               fields=['name','item_code', 'item_name', 'description','standard_rate', 'stock_uom', 'is_stock_item','image','item_name_arabic','item_group'])
		item_tax_templates = frappe.get_all('Item Tax Template Detail',fields=['parent AS item_tax_template', 'tax_type', 'tax_rate'])
		stock_counts = frappe.get_all('Bin', fields=['item_code', 'actual_qty'], filters={'item_code': ['in', [item['item_code'] for item in items]]})
		stock_count_dict = {stock['item_code']: stock['actual_qty'] for stock in stock_counts}
		barcodes = frappe.get_all('Item Barcode',fields=['parent','barcode','barcode_type','uom'])
		### creating barcode dict


		barcode_dict = {}

		for barcode in barcodes:
			parent = barcode['parent']
			# Create a dictionary entry for the parent if it doesn't exist
			if parent not in barcode_dict:
				barcode_dict[parent] = []# Initialize an empty list for barcodes
				
			
			# Append the current barcode information to the list
			barcode_dict[parent].append({
				'barcode': barcode['barcode'],
				'barcode_type': barcode['barcode_type'],
				'uom': barcode['uom']
			})


		tax_template_dict = {}
		for template in item_tax_templates:
			if template['item_tax_template'] not in tax_template_dict:
				tax_template_dict[template['item_tax_template']] = []
			tax_template_dict[template['item_tax_template']].append({
                'tax_type': template['tax_type'],
                'tax_rate': template['tax_rate']
            })
		item_prices = frappe.get_all('Item Price',
                                     fields=['item_code', 'price_list_rate','uom'],
                                     filters={'item_code': ['in', [item['item_code'] for item in items]]})
		# item_lookup = {item_prices['item_code']: item_prices['price_list_rate'] for item_prices in item_prices}
		item_lookup = {}

		for item_price in item_prices:
			item_code = item_price['item_code']
			print(item_code)
			if item_code not in item_lookup:
				item_lookup[item_code] = []
			
			# Append the current barcode information to the list
			item_lookup[item_code].append(
				item_price
			)

		# item_group_tax_template = frappe.get_all('Item Group',
        #                                              fields=['name'])
		# for i in item_group_tax_template:
		# 	item_group_taxes = frappe.db.get_all(
		# 		'Item Tax Template Detail',
		# 		filters={'parent': i['name']},  # Parent is the Item Group name
		# 		fields=['tax_type', 'tax_rate']
		# 	)
		# 	print(item_group_taxes,"sdssdsdssd")
		item_groups = frappe.get_all('Item Group', fields=['name'])
		group_tax = {}
		for group in item_groups:
	# Get the Item Tax Template assigned to the Item Group
			item_group_tax_templates = frappe.db.get_all(
				'Item Tax',
				filters={'parent': group['name']},  # Assuming 'parent' links the Item Group to the Item Tax table
				fields=['item_tax_template']
			)

			if item_group_tax_templates:
				for template in item_group_tax_templates:
					# Get the details of the tax for the template
					item_group_taxes = frappe.db.get_all(
						'Item Tax Template Detail',
						filters={'parent': template['item_tax_template']},
						fields=['tax_type', 'tax_rate']
					)
					group_tax[group['name']] = item_group_taxes[0]

			else:
				group_tax[group['name']] = []
		for item in items:
			item['barcode_details'] = barcode_dict.get(item['name'],[])


			if item['item_code'] in item_lookup:
				item['price'] = item_lookup[item['item_code']]
			try:
				if item['item_group'] in group_tax and group_tax[item['item_group']]:
					item['taxes'] = group_tax[item['item_group']]
				else :
					tax_type = frappe.get_all('Item Tax', filters={'parent': item['item_code']}, fields=['item_tax_template'])
					item['taxes'] = tax_template_dict.get(tax_type[0]['item_tax_template'], [])
			except Exception as e:
				item['taxes'] = []  # Handle missing taxes or errors
			item['stock_count'] = stock_count_dict.get(item['item_code'], 0)  # Default to 0 if no stock found
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


@frappe.whitelist(allow_guest=False)
def get_pos_profile_and_printer_configs(user):
    try:
        # Find POS Profiles where the given user is listed in the "POS Profile User" child table
        applicable_pos_profiles = frappe.db.get_value(
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