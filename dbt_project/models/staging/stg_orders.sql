{{ config(materialized='external', location="gcs://{{ env_var('GCS_BUCKET_NAME') }}/data/stg_orders.parquet") }}
with source as (

    {#-
    Normally we would select from the table here, but we are using seeds to load
    our data in this project
    #}
    select * from "gcs://{{ env_var('GCS_BUCKET_NAME') }}/data/raw_orders.csv"

),

renamed as (

    select
        id as order_id,
        user_id as customer_id,
        order_date,
        status

    from source

)

select * from renamed
