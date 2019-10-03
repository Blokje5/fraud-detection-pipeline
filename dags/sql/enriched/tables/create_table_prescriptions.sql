CREATE TABLE enriched.PRESCRIPTIONS AS
SELECT CONCAT(npi, drug_name) AS ID,
    drug_name AS DRUG_ID,
    npi AS PROVIDER_ID
    total_claim_count AS CLAIM_COUNT,
    bene_count AS BENEFICIARY_COUNT