frappe.ui.form.on("AMC Contract", {
    refresh(frm) {
        if (frm.doc.docstatus === 1 && frm.doc.status === "Active") {
            frm.add_custom_button(__("Create Service Request"), () => {
                frappe.new_doc("Service Request", {
                    customer: frm.doc.customer,
                });
            });
        }
    },
});