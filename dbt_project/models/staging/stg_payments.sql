{{ config(materialized='external', location="gcs://{{ env_var('GCS_BUCKET_NAME') }}/data/stg_payments.parquet") }}
with source as (
    
    {#-
    Normally we would select from the table here, but we are using seeds to load
    our data in this project
    #}
    select * from "gcs://{{ env_var('GCS_BUCKET_NAME') }}/data/raw_payments.csv"

),

renamed as (

    select
        id as payment_id,
        order_id,
        payment_method,

        -- `amount` is currently stored in cents, so we convert it to dollars
        amount / 100 as amount

    from source

)

select * from renamed
