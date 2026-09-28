select distinct
    repository_id as repository_key,
    repository_id,
    repository_provider as provider,
    provider_repository_id,
    repository_name as canonical_full_name,
    identity_status
from {{ ref('stg_pulse__memberships') }}
