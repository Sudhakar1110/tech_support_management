# TechCare

Device service, repair and AMC management app for Frappe / ERPNext.

Features: Service Requests with SLA tracking, Devices, AMC Contracts with auto-generated visit schedules, Service Reports with parts and photos, Technician Profiles, a mobile technician portal at /technician, script reports, and a customer-facing print format.

Requires ERPNext (uses Customer and Item doctypes).

## Install

    bench get-app techcare /path/to/techcare
    bench --site yoursite.local install-app techcare
    bench --site yoursite.local migrate
    bench build && bench restart