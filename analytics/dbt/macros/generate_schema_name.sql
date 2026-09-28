{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- if custom_schema_name is none -%}
        {{ target.schema }}
    {%- elif custom_schema_name | trim in ['dbt_staging', 'dbt_intermediate', 'dbt_test__audit', 'analytics'] -%}
        {{ custom_schema_name | trim }}
    {%- else -%}
        {{ exceptions.raise_compiler_error('Unexpected dbt schema: ' ~ custom_schema_name) }}
    {%- endif -%}
{%- endmacro %}
