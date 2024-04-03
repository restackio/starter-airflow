{{ config(materialized='external', location="gcs://{{ env_var('GCS_BUCKET_NAME') }}/data/stg_customers.parquet") }}
with source as (

    {#-
    Normally we would select from the table here, but we are using seeds to load
    our data in this project
    #}
    select * from "gcs://{{ env_var('GCS_BUCKET_NAME') }}/data/raw_customers.csv"

),

renamed as (

    select
        id as customer_id,
        first_name,
        last_name

    from source

)

select * from renamed
