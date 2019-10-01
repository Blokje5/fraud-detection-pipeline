SELECT  CASE WHEN count(distinct id)= count(id)
THEN true ELSE false END
FROM enriched.PROVIDER_DIM