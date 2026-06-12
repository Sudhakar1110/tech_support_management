import frappe
from frappe import _

def execute(filters=None):
    filters = filters or {}
    return get_columns(), get_data(filters)

def get_columns():
    return [
        {"fieldname": "technician", "label": _("Technician"),
         "fieldtype": "Link", "options": "Technician Profile", "width": 180},
        {"fieldname": "technician_name", "label": _("Name"),
         "fieldtype": "Data", "width": 160},
        {"fieldname": "total_jobs", "label": _("Total Jobs"),
         "fieldtype": "Int", "width": 100},
        {"fieldname": "resolved", "label": _("Resolved"),
         "fieldtype": "Int", "width": 100},
        {"fieldname": "sla_breached", "label": _("SLA Breached"),
         "fieldtype": "Int", "width": 110},
        {"fieldname": "avg_resolution_hours", "label": _("Avg Resolution (hrs)"),
         "fieldtype": "Float", "precision": 1, "width": 150},
        {"fieldname": "avg_rating", "label": _("Avg Rating"),
         "fieldtype": "Float", "precision": 2, "width": 110},
    ]

def get_data(filters):
    conditions = ""
    values = {}
    if filters.get("from_date"):
        conditions += " and sr.creation >= %(from_date)s"
        values["from_date"] = filters["from_date"]
    if filters.get("to_date"):
        conditions += " and sr.creation <= %(to_date)s"
        values["to_date"] = filters["to_date"]

    return frappe.db.sql(f"""
        select
            sr.assigned_technician as technician,
            tp.technician_name,
            count(sr.name) as total_jobs,
            sum(case when sr.status in ('Resolved', 'Closed') then 1 else 0 end) as resolved,
            sum(case when sr.sla_status = 'Breached' then 1 else 0 end) as sla_breached,
            avg(case when sr.resolved_on is not null
                then timestampdiff(minute, sr.creation, sr.resolved_on) / 60.0
                end) as avg_resolution_hours,
            avg(nullif(sr.customer_rating, 0)) as avg_rating
        from `tabService Request` sr
        inner join `tabTechnician Profile` tp on tp.name = sr.assigned_technician
        where sr.assigned_technician is not null {conditions}
        group by sr.assigned_technician, tp.technician_name
        order by resolved desc
    """, values, as_dict=True)