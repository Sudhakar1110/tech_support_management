import frappe
from frappe.utils import add_to_date, now_datetime, nowdate

def check_sla_breaches():
    """Hourly: mark open requests as At Risk / Breached based on sla_due."""
    now = now_datetime()
    at_risk_cutoff = add_to_date(now, hours=2)
    open_statuses = ("Open", "Assigned", "In Progress", "Waiting for Parts")

    # Breached
    frappe.db.sql("""
        update `tabService Request`
        set sla_status = 'Breached'
        where status in %(statuses)s
          and sla_due is not null and sla_due < %(now)s
          and sla_status != 'Breached'
    """, {"statuses": open_statuses, "now": now})

    # At Risk (due within 2 hours)
    frappe.db.sql("""
        update `tabService Request`
        set sla_status = 'At Risk'
        where status in %(statuses)s
          and sla_due is not null
          and sla_due >= %(now)s and sla_due < %(cutoff)s
          and sla_status = 'On Track'
    """, {"statuses": open_statuses, "now": now, "cutoff": at_risk_cutoff})

    frappe.db.commit()

def update_amc_status():
    """Daily: expire active contracts past their end date."""
    expired = frappe.get_all(
        "AMC Contract",
        filters={"docstatus": 1, "status": "Active", "end_date": ["<", nowdate()]},
        pluck="name",
    )
    for name in expired:
        frappe.db.set_value("AMC Contract", name, "status", "Expired")
    frappe.db.commit()

def notify_expiring_amcs():
    """Daily: email Service Managers about contracts expiring in 30 days."""
    expiring = frappe.get_all(
        "AMC Contract",
        filters={
            "docstatus": 1,
            "status": "Active",
            "end_date": ["between", [nowdate(), add_to_date(nowdate(), days=30)]],
        },
        fields=["name", "customer_name", "end_date"],
    )
    if not expiring:
        return

    managers = frappe.get_all(
        "Has Role",
        filters={"role": "Service Manager", "parenttype": "User"},
        pluck="parent",
    )
    recipients = [
        u for u in set(managers)
        if frappe.db.get_value("User", u, "enabled") and u != "Administrator"
    ]
    if not recipients:
        return

    rows = "".join(
        f"<tr><td>{d.name}</td><td>{d.customer_name}</td><td>{d.end_date}</td></tr>"
        for d in expiring
    )
    frappe.sendmail(
        recipients=recipients,
        subject=f"{len(expiring)} AMC contract(s) expiring within 30 days",
        message=f"""
            <p>The following AMC contracts are expiring soon:</p>
            <table border="1" cellpadding="6" cellspacing="0">
              <tr><th>Contract</th><th>Customer</th><th>End Date</th></tr>
              {rows}
            </table>
        """,
    )