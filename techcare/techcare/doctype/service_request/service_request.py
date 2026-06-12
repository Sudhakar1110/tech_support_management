import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_to_date, now_datetime

SLA_FIELD_MAP = {
    "Critical": "critical_sla_hours",
    "High": "high_sla_hours",
    "Medium": "medium_sla_hours",
    "Low": "low_sla_hours",
}

DEFAULT_SLA_HOURS = {"Critical": 4, "High": 8, "Medium": 24, "Low": 72}

class ServiceRequest(Document):
    def validate(self):
        self.set_sla_due()
        self.sync_status_with_assignment()
        self.validate_rating()
        self.set_resolved_on()

    def set_sla_due(self):
        if self.sla_due:
            return
        settings = frappe.get_cached_doc("TechCare Settings")
        field = SLA_FIELD_MAP.get(self.priority, "medium_sla_hours")
        hours = settings.get(field) or DEFAULT_SLA_HOURS.get(self.priority, 24)
        base = self.creation or now_datetime()
        self.sla_due = add_to_date(base, hours=int(hours))

    def sync_status_with_assignment(self):
        if self.assigned_technician and self.status == "Open":
            self.status = "Assigned"
        if not self.assigned_technician and self.status == "Assigned":
            self.status = "Open"

    def validate_rating(self):
        if self.customer_rating and not (1 <= int(self.customer_rating) <= 5):
            frappe.throw(_("Customer Rating must be between 1 and 5"))

    def set_resolved_on(self):
        if self.status in ("Resolved", "Closed") and not self.resolved_on:
            self.resolved_on = now_datetime()
        if self.status not in ("Resolved", "Closed"):
            self.resolved_on = None