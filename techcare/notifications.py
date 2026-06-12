import frappe


def get_notification_config():
    return {
        "for_doctype": {
            "Service Request": {
                "events": ["Threshold", "Status Change", "Mention", "Assignment"],
                "filter": {"status": ["Open", "Assigned", "In Progress", "At Risk", "Breached"]},
            },
            "AMC Contract": {
                "events": ["Days Left", "Status Change"],
                "filter": {"status": ["Active"]},
            },
        }
    }