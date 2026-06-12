import frappe
from frappe import _

def execute(filters=None):
    filters = filters or {}
    days = int(filters.get("within_days") or 60)

    columns = [
        {"fieldname": "name", "label": _("AMC Contract"),
         "fieldtype": "Link", "options": "AMC Contract", "width": 160},
        {"fieldname": "customer_name", "label": _("Customer"),
         "fieldtype": "Data", "width": 200},
        {"fieldname": "end_date", "label": _("Expires On"),
         "fieldtype": "Date", "width": 110},
        {"fieldname": "days_left", "label": _("Days Left"),
         "fieldtype": "Int", "width": 90},
        {"fieldname": "contract_value", "label": _("Contract Value"),
         "fieldtype": "Currency", "width": 130},
        {"fieldname": "devices_covered", "label": _("Devices"),
         "fieldtype": "Int", "width": 80},
    ]

    data = frappe.db.sql("""
        select
            ac.name, ac.customer_name, ac.end_date,
            datediff(ac.end_date, curdate()) as days_left,
            ac.contract_value,
            (select count(*) from `tabAMC Covered Device` cd
             where cd.parent = ac.name) as devices_covered
        from `tabAMC Contract` ac
        where ac.docstatus = 1
          and ac.status = 'Active'
          and ac.end_date between curdate()
              and date_add(curdate(), interval %(days)s day)
        order by ac.end_date asc
    """, {"days": days}, as_dict=True)

    return columns, data