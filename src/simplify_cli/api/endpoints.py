BASE_URL = "https://api.simplify.jobs/v2"

# Auth / Profile
ME = f"{BASE_URL}/candidate/me"
PREFERENCES = f"{ME}/preferences"
RESUMES = f"{ME}/resume"

# Tracker
TRACKER = f"{ME}/tracker"
TRACKER_JOB = f"{TRACKER}/job-posting"  # /{id}
TRACKER_SAVE = f"{TRACKER}/dunder/save"
TRACKER_APPLIED = f"{TRACKER}/dunder/applied"
TRACKER_STATUS_UPDATE = f"{TRACKER}/status-update-action"
TRACKER_EXPORT_CSV = f"{TRACKER}/export/csv"
TRACKER_SANKEY = f"{TRACKER}/sankey"

# Job details
JOB_POSTING = f"{BASE_URL}/job-posting"  # /:id/{uuid}/company, /:id/{uuid}/history

# Typesense
TYPESENSE_HOST = "https://js-ha.simplify.jobs"
TYPESENSE_SEARCH = f"{TYPESENSE_HOST}/multi_search"
TYPESENSE_API_KEY = "SWF1ODFZbzBkcVlVdnVwT2FqUE5EZ3JpSk5hVmdpUHg1SklXWEdGbHZVRT1POHJieyJleGNsdWRlX2ZpZWxkcyI6ImNvbXBhbnlfdXJsLGNhdGVnb3JpZXMsYWRkaXRpb25hbF9yZXF1aXJlbWVudHMsY291bnRyaWVzLGRlZ3JlZXMsZ2VvbG9jYXRpb25zLGluZHVzdHJpZXMsaXNfc2ltcGxlX2FwcGxpY2F0aW9uLGpvYl9saXN0cyxsZWFkZXJzaGlwX3R5cGUsc2VjdXJpdHlfY2xlYXJhbmNlLHNraWxscyx1cmwifQ=="
TYPESENSE_COLLECTION = "jobs"
