from prometheus_client import Counter, Histogram, Gauge

MEMORY_MERGES_TOTAL = Counter(
    "scoutos_memory_merges_total", "Total number of memory merge operations"
)

MEMORY_REPAIR_LATENCY_SECONDS = Histogram(
    "scoutos_memory_repair_latency_seconds",
    "Latency of memory repair operations",
    buckets=(0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 2, 5),
)

ACTIVE_USERS_TOTAL = Gauge("scoutos_active_users_total", "Current number of active users")

UNAUTHORIZED_ACCESS_TOTAL = Counter(
    "scoutos_unauthorized_access_total", "Count of unauthorized access attempts"
)

STORAGE_USED_BYTES = Gauge("scoutos_storage_used_bytes", "Storage used in bytes")
STORAGE_TOTAL_BYTES = Gauge("scoutos_storage_total_bytes", "Total storage available in bytes")

USER_SESSIONS_TOTAL = Counter(
    "scoutos_user_sessions_total",
    "Total user sessions by language",
    ['user_language'],
)

CONSENT_PROMPTED_TOTAL = Counter("scoutos_consent_prompted_total", "Number of consent prompts shown")
CONSENT_ACCEPTED_TOTAL = Counter("scoutos_consent_accepted_total", "Number of consents accepted")
