frappe.query_reports["AMC Expiry"] = {
    filters: [
        {
            fieldname: "within_days",
            label: __("Expiring Within (Days)"),
            fieldtype: "Int",
            default: 60,
        },
    ],
};