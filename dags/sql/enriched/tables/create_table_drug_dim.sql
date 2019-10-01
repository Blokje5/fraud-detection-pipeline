CREATE TABLE enriched.DRUG_DIM AS
SELECT DISTINCT drug_name, generic_name 
FROM staging.npi_drug 