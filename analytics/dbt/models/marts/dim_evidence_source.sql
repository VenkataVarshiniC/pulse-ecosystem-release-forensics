with represented as (
    select source_id from {{ ref('stg_pulse__collection_tasks') }}
    union
    select source_id from {{ ref('stg_pulse__artifacts') }}
), capture_methods as (
    select
        source_id,
        count(*) filter (where capture_method = 'collector') as collector_capture_count,
        count(*) filter (where capture_method = 'connector_assisted')
            as connector_assisted_capture_count,
        count(*) filter (where capture_method = 'fixture') as fixture_capture_count
    from {{ ref('stg_pulse__artifacts') }}
    group by source_id
)
select
    s.source_id as source_key,
    s.source_id,
    s.provider,
    s.source_type,
    s.source_version,
    s.base_locator,
    s.access_class,
    coalesce(c.collector_capture_count, 0) as collector_capture_count,
    coalesce(c.connector_assisted_capture_count, 0) as connector_assisted_capture_count,
    coalesce(c.fixture_capture_count, 0) as fixture_capture_count
from {{ source('pulse_ingestion', 'source_registry') }} s
join represented r on s.source_id = r.source_id
left join capture_methods c on s.source_id = c.source_id
