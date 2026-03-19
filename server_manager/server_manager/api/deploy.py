import frappe
import subprocess

@frappe.whitelist()
def deploy(server, branch):
    server_doc = frappe.get_doc("Server", server)

    log = frappe.get_doc({
        "doctype": "Deployment Log",
        "server": server,
        "branch": branch,
        "status": "Running",
        "triggered_by": frappe.session.user
    }).insert(ignore_permissions=True)

    try:
        commands = f"""
        cd {server_doc.bench_path}
        cd apps/{server_doc.app_name}

        git fetch origin
        git checkout {branch}
        git pull origin {branch}

        cd ../../

        bench --site {server_doc.site_name} migrate
        bench --site {server_doc.site_name} clear-cache
        bench restart
        """

        result = subprocess.run(
            commands,
            shell=True,
            capture_output=True,
            text=True
        )

        log.log = result.stdout + "\n" + result.stderr

        if result.returncode == 0:
            log.status = "Success"
        else:
            log.status = "Failed"

        log.save(ignore_permissions=True)

        return log.status

    except Exception as e:
        log.status = "Failed"
        log.log = str(e)
        log.save(ignore_permissions=True)
        frappe.throw(str(e))