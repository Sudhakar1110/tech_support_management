frappe.ui.form.on("Service Request", {
    refresh(frm) {
        if (!frm.is_new() && !["Resolved", "Closed", "Cancelled"].includes(frm.doc.status)) {
            frm.add_custom_button(__("Create Service Report"), () => {
                frappe.new_doc("Service Report", {
                    service_request: frm.doc.name,
                    customer: frm.doc.customer,
                    device: frm.doc.device,
                });
            });
        }

        if (frm.doc.sla_status === "Breached") {
            frm.dashboard.set_headline(
                `<span class="indicator red">${__("SLA Breached")}</span>`
            );
        }
    },

    priority(frm) {
        frm.set_value("sla_due", null);
    },
});