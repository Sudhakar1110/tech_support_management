import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_months, getdate, nowdate

FREQUENCY_MONTHS = {
    "Monthly": 1,
    "Quarterly": 3,
    "Half-Yearly": 6,
    "Yearly": 12,
}


class AMCContract(Document):
    def validate(self):
        if getdate(self.end_date) <= getdate(self.start_date):
            frappe.throw(_("End Date must be after Start Date"))
        if not self.covered_devices:
            frappe.throw(_("Add at least one covered device"))

    def on_submit(self):
        self.generate_visit_schedule()
        self.db_set(
            "status",
            "Active" if getdate(self.end_date) >= getdate(nowdate()) else "Expired",
        )

    def on_cancel(self):
        self.db_set("status", "Cancelled")

    def generate_visit_schedule(self):
        if self.visit_schedule:
            return

        months = FREQUENCY_MONTHS.get(self.visit_frequency, 3)
        visit_date = getdate(self.start_date)
        end = getdate(self.end_date)

        while visit_date <= end:
            self.append("visit_schedule", {
                "scheduled_date": visit_date,
                "status": "Scheduled",
            })
            visit_date = add_months(visit_date, months)

        self.save()


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