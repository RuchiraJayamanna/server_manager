// Copyright (c) 2026, Ruchira Jayamanna and contributors
// For license information, please see license.txt

frappe.ui.form.on('Server', {
    refresh(frm) {
        frm.add_custom_button('Deploy', () => {
            frappe.prompt([
                {
                    fieldname: 'branch',
                    label: 'Branch Name',
                    fieldtype: 'Data',
                    default: frm.doc.branch,
                    reqd: 1
                }
            ], (values) => {

                frappe.call({
                    method: 'server_manager.server_manager.api.deploy.deploy',
                    args: {
                        server: frm.doc.name,
                        branch: values.branch
                    },
                    freeze: true,
                    freeze_message: "Deploying..."
                }).then(r => {
                    frappe.msgprint("Deployment " + r.message);
                });

            }, "Deploy Server", "Start");
        });
    }
});