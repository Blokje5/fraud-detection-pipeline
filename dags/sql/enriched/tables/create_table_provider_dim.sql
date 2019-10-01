CREATE TABLE enriched.PROVIDER_DIM AS
SELECT DISTINCT npi as ID, 
nppes_provider_last_org_name AS last_or_organisation_name,
nppes_provider_first_name as first_name,
nppes_provider_city as city,
nppes_provider_state as state,
specialty_description as speciality
FROM staging.npi_drug 