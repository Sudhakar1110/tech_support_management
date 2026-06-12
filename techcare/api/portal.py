import frappe
from frappe import _

ACTION_MAP = {
    "start": "In Progress",
    "parts": "Waiting for Parts",
    "resume": "In Progress",
    "resolve": "Resolved",
}

@frappe.whitelist()
def update_job_status(service_request, action):
    """Status transitions from the technician portal, with ownership check."""
    if action not in ACTION_MAP:
        frappe.throw(_("Invalid action"))

    doc = frappe.get_doc("Service Request", service_request)

    technician = frappe.db.get_value(
        "Technician Profile", {"user": frappe.session.user}, "name"
    )
    if doc.assigned_technician != technician and "Service Manager" not in frappe.get_roles():
        frappe.throw(_("You are not assigned to this Service Request"),
                     frappe.PermissionError)

    doc.status = ACTION_MAP[action]
    if action == "resolve":
        doc.resolved_on = frappe.utils.now_datetime()
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    return {"status": doc.status}