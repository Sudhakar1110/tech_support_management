import frappe
from frappe.model.document import Document

class TechnicianProfile(Document):
    def validate(self):
        if self.user:
            roles = frappe.get_roles(self.user)
            if "Service Technician" not in roles:
                user = frappe.get_doc("User", self.user)
                user.append("roles", {"role": "Service Technician"})
                user.save(ignore_permissions=True)