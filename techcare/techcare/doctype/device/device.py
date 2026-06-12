import frappe
from frappe import _
from frappe.model.document import Document

class Device(Document):
    def validate(self):
        if self.serial_number:
            duplicate = frappe.db.exists(
                "Device",
                {"serial_number": self.serial_number, "name": ["!=", self.name]},
            )
            if duplicate:
                frappe.throw(
                    _("Serial Number {0} already exists on Device {1}").format(
                        self.serial_number, duplicate
                    )
                )