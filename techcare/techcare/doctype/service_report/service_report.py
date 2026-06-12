import frappe
from frappe.model.document import Document
from frappe.utils import flt, now_datetime


class ServiceReport(Document):
    def validate(self):
        self.calculate_totals()

    def calculate_totals(self):
        total = 0
        for row in self.spare_parts:
            row.amount = flt(row.qty) * flt(row.rate)
            total += row.amount
        self.total_parts_amount = total

    def on_submit(self):
        if self.mark_request_resolved and self.service_request:
            sr = frappe.get_doc("Service Request", self.service_request)
            if sr.status not in ("Resolved", "Closed", "Cancelled"):
                sr.status = "Resolved"
                sr.resolved_on = now_datetime()
                sr.save()


def get_permission_query_conditions(user):
    if not user:
        user = frappe.session.user
    
    if "System Manager" in frappe.get_roles(user):
        return None
    
    if "Service Manager" in frappe.get_roles(user):
        return None
    
    return "1 = 0"


def has_permission(doc, ptype, user):
    if not user:
        user = frappe.session.user
    
    if "System Manager" in frappe.get_roles(user):
        return True
    
    if "Service Manager" in frappe.get_roles(user):
        return True
    
    return False