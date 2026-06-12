import frappe
from frappe import _

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw(_("Please login to access the technician portal"),
                     frappe.PermissionError)

    technician = frappe.db.get_value(
        "Technician Profile", {"user": frappe.session.user}, "name"
    )
    if not technician:
        frappe.throw(_("No Technician Profile is linked to your user account"))

    context.no_cache = 1
    context.technician = technician
    context.technician_name = frappe.db.get_value(
        "Technician Profile", technician, "technician_name"
    )
    context.jobs = get_assigned_jobs(technician)
    return context

def get_assigned_jobs(technician):
    return frappe.get_all(
        "Service Request",
        filters={
            "assigned_technician": technician,
            "status": ["in", ["Assigned", "In Progress", "Waiting for Parts"]],
        },
        fields=[
            "name", "customer_name", "device", "status", "priority",
            "issue_description", "sla_due", "creation",
        ],
        order_by="""
            CASE priority
                WHEN 'Critical' THEN 0
                WHEN 'High' THEN 1
                WHEN 'Medium' THEN 2
                ELSE 3
            END, sla_due asc
        """,
    )