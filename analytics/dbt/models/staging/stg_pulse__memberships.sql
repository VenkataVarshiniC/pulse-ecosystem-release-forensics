select
    m.case_version_id,
    m.repository_id,
    r.provider as repository_provider,
    r.provider_repository_id,
    r.canonical_full_name as repository_name,
    r.identity_status,
    m.selection_method,
    m.eligibility_status,
    m.selection_rationale,
    m.included_at
from {{ source('pulse_core', 'cohort_membership') }} m
join {{ source('pulse_core', 'repository') }} r
    on m.repository_id = r.repository_id
