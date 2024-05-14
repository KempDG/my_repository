# Databricks notebook source
# MAGIC %md
# MAGIC ## ICE_AAS.TBL_AAS_WITNESS

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC DROP TABLE IF EXISTS ICE_AAS.TBL_AAS_WITNESS;
# MAGIC
# MAGIC CREATE TABLE ICE_AAS.TBL_AAS_WITNESS AS (
# MAGIC SELECT 
# MAGIC DISTINCT
# MAGIC ROW_NUMBER () OVER (PARTITION BY TCP.CLAIM_ID ORDER BY PARTY_ID ASC) AS WitnessNumber,
# MAGIC TCP.CLAIM_ID,
# MAGIC DC.CLAIM_NUMBER,
# MAGIC PARTY_ID,
# MAGIC
# MAGIC FORENAME,
# MAGIC SURNAME,
# MAGIC
# MAGIC POSTAL_ADDRESS,
# MAGIC
# MAGIC POSTCODE,
# MAGIC EMAIL,
# MAGIC       
# MAGIC DAYTIME_PHONE,
# MAGIC EVENING_PHONE,
# MAGIC MOBILE
# MAGIC
# MAGIC
# MAGIC   FROM hive_metastore.ice_aas.ice_dim_claim_party DCP
# MAGIC
# MAGIC     INNER JOIN hive_metastore.ice_aas.ice_trn_claim_party TCP ON DCP.PARTY_ID = TCP.CLAIM_PARTY_ID AND TCP.CURRENT_FLAG = 'Y' AND NATURE = 'Witness'
# MAGIC   
# MAGIC   LEFT JOIN hive_metastore.ice_aas.ice_dim_object_vehicle DOV ON TCP.VEHICLE_ID = DOV.VEHICLE_ID AND DOV.CURRENT_FLAG = 'Y'
# MAGIC
# MAGIC   INNER JOIN hive_metastore.ice_aas.ice_dim_claim DC ON TCP.CLAIM_ID = DC.CLAIM_ID AND DC.CURRENT_FLAG = 'Y'
# MAGIC
# MAGIC  WHERE 
# MAGIC  DCP.CURRENT_FLAG = 'Y'
# MAGIC
# MAGIC ORDER BY CLAIM_ID ASC 
# MAGIC )
# MAGIC
# MAGIC
# MAGIC
# MAGIC