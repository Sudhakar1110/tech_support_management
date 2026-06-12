import frappe

DEFAULT_CATEGORIES = [
    "Laptop", "Desktop", "Printer", "Server", "Networking", "UPS", "Other",
]

def after_install():
    create_roles()
    create_device_categories()

def create_roles():
    for role in ("Service Manager", "Service Technician"):
        if not frappe.db.exists("Role", role):
            frappe.get_doc({
                "doctype": "Role",
                "role_name": role,
                "desk_access": 1,
            }).insert(ignore_permissions=True)

def create_device_categories():
    for cat in DEFAULT_CATEGORIES:
        if not frappe.db.exists("Device Category", cat):
            frappe.get_doc({
                "doctype": "Device Category",
                "category_name": cat,
            }).insert(ignore_permissions=True)