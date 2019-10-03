WITH AGGREGATE_PAYMENTS AS (
    SELECT Physician_Profile_ID AS ID, SUM(Total_Amount_of_Payment_USDollars) AS AMOUNT
    FROM staging.PAYMENTS
    GROUP BY Physician_Profile_ID
)
CREATE TABLE enriched.PROVIDER_DIM AS
SELECT DISTINCT NPI.npi as ID, 
NPI.nppes_provider_last_org_name AS last_or_organisation_name,
NPI.nppes_provider_first_name as first_name,
NPI.nppes_provider_city as city,
NPI.nppes_provider_state as state,
NPI.specialty_description as speciality
AGGREGATE_PAYMENTS.AMOUNT as amount
FROM staging.npi_drug NPI
INNER JOIN AGGREGATE_PAYMENTS ON AGGREGATE_PAYMENTS.ID = NPI.npi