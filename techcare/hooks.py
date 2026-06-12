app_name = "techcare"
app_title = "TechCare"
app_publisher = "TechCare"
app_description = "Device service, repair & AMC management"
app_email = "admin@example.com"
app_license = "MIT"

after_install = "techcare.install.after_install"

scheduler_events = {
    "hourly": [
        "techcare.tasks.check_sla_breaches",
    ],
    "daily": [
        "techcare.tasks.update_amc_status",
        "techcare.tasks.notify_expiring_amcs",
    ],
}

website_route_rules = [
    {"from_route": "/technician", "to_route": "technician"},
]