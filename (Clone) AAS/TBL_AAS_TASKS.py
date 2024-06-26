# Databricks notebook source
# MAGIC %md
# MAGIC ## ICE_AAS.TBL_AAS_TASKS

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC DROP TABLE IF EXISTS ICE_AAS.TBL_AAS_TASKS;
# MAGIC
# MAGIC CREATE TABLE ICE_AAS.TBL_AAS_TASKS AS (
# MAGIC
# MAGIC SELECT DISTINCT
# MAGIC DC.CLAIM_NUMBER as Claim_Number,
# MAGIC CS.Workstream AS Workstream,
# MAGIC DC.Subrogated,
# MAGIC DC.NOTIFICATION_DATE as Notification_Date,
# MAGIC DC.EVENT_DATE as Incident_Date,
# MAGIC DT.TASK_NAME,
# MAGIC DT.task_id,
# MAGIC WG.WORKGROUP_DESCRIPTION,
# MAGIC US.FULL_USERNAME as Task_Handler,
# MAGIC US.TEAM_DESCRIPTION as Task_Handler_Team,
# MAGIC TASK.CREATEDDATE as Date_Task_Added,
# MAGIC TT.PERFORMED_DATE AS Date_Task_Last_Worked,
# MAGIC TT.TASK_TRANSACTION_TYPE_CODE AS TaskStatus,
# MAGIC TRANTCURRENT.task_transaction_type_description as CurrentStatus,
# MAGIC TT.due_date,
# MAGIC TT.Deferred_Date,
# MAGIC DEF.DeferredBy,
# MAGIC DateTaskDeferred,
# MAGIC
# MAGIC case 
# MAGIC when TT.TASK_TRANSACTION_TYPE_CODE = 'CREATED' and TT.CURRENT_FLAG ='Y' then TT.DUE_DATE
# MAGIC when TT.TASK_TRANSACTION_TYPE_CODE = 'UNASSIGNED' and TT.CURRENT_FLAG ='Y' then TT.DUE_DATE
# MAGIC WHEN TT.TASK_TRANSACTION_TYPE_CODE = 'Deferred' and TT.CURRENT_FLAG ='Y' then TT.deferred_date
# MAGIC WHEN TT.TASK_TRANSACTION_TYPE_CODE = 'Completed' then NULL 
# MAGIC end as Diary_Date, 
# MAGIC
# MAGIC case 
# MAGIC when TT.TASK_TRANSACTION_TYPE_CODE = 'CREATED' and TT.CURRENT_FLAG ='Y' then DT.ACTIVATETIME
# MAGIC WHEN TT.TASK_TRANSACTION_TYPE_CODE = 'Deferred' and TT.CURRENT_FLAG ='Y' then DT.ACTIVATETIME
# MAGIC WHEN TT.TASK_TRANSACTION_TYPE_CODE = 'Completed' then NULL end as Task_Active_Date, 
# MAGIC TT.DATE_COMPLETED as Date_Task_Completed
# MAGIC
# MAGIC
# MAGIC
# MAGIC FROM hive_metastore.ice_aas.ice_trn_task TT
# MAGIC INNER JOIN hive_metastore.ice_aas.ice_trn_task TTCURRENT ON TT.TASK_ID = TTCURRENT.TASK_ID AND TTCURRENT.CURRENT_FLAG = 'Y'
# MAGIC LEFT JOIN hive_metastore.ice_aas.ice_dim_task_transaction_type TRANTCURRENT ON TTCURRENT.TASK_TRANSACTION_TYPE_KEY = TRANTCURRENT.TASK_TRANSACTION_TYPE_KEY 
# MAGIC LEFT JOIN hive_metastore.ice_aas.ice_dim_task DT ON TT.TASK_ID = DT.TASK_ID
# MAGIC LEFT JOIN hive_metastore.ice_aas.ice_dim_task_transaction_type TRANT ON TT.TASK_TRANSACTION_TYPE_KEY = TRANT.TASK_TRANSACTION_TYPE_KEY 
# MAGIC LEFT JOIN hive_metastore.ice_aas.ice_dim_user US ON TT.USER_PARTY_ID = US.USER_PARTY_ID
# MAGIC LEFT JOIN hive_metastore.ice_aas.ice_dim_claim DC ON TT.CLAIM_ID = DC.CLAIM_ID
# MAGIC LEFT JOIN hive_metastore.ice_aas.ice_dim_workgroup DW ON TTCURRENT.WORKGROUP_ID = DW.WORKGROUP_ID
# MAGIC LEFT JOIN hive_metastore.ice_aas.ice_dim_task_status DTS ON DTS.TASK_STATUS_KEY = TT.TASK_STATUS_KEY AND TT.CURRENT_FLAG = 'Y'
# MAGIC LEFT JOIN hive_metastore.ice_aas.tbl_aas_claim_summary CS ON CS.CLAIM_ID=DC.CLAIM_ID
# MAGIC LEFT OUTER JOIN hive_metastore.ice_aas.ice_dim_workgroup WG ON WG.WORKGROUP_ID = TT.WORKGROUP_ID 
# MAGIC
# MAGIC LEFT JOIN ( 
# MAGIC SELECT
# MAGIC task_id,
# MAGIC MAX(performed_date) as DateTaskDeferred,
# MAGIC MAX(full_username) as DeferredBy
# MAGIC FROM hive_metastore.ice_aas.ice_trn_task TT 
# MAGIC LEFT JOIN hive_metastore.ice_aas.ice_dim_user DU ON TT.user_party_id = DU.user_party_id and DU.CURRENT_FLAG = 'Y'
# MAGIC Where task_transaction_type_code = 'DEFERRED'
# MAGIC group by task_id
# MAGIC ) DEF ON DEF.task_id = TT.task_id
# MAGIC
# MAGIC LEFT JOIN
# MAGIC (
# MAGIC SELECT *
# MAGIC FROM (
# MAGIC SELECT 
# MAGIC TASK_KEY,
# MAGIC TRANSACTION_DATE AS CREATEDDATE,
# MAGIC ROW_NUMBER() OVER (PARTITION BY TASK_KEY ORDER BY TRANSACTION_DATE ASC) AS RN
# MAGIC FROM hive_metastore.ice_aas.ice_trn_task TTCREATE
# MAGIC WHERE TASK_TRANSACTION_TYPE_CODE='CREATED'
# MAGIC )main WHERE RN=1
# MAGIC )TASK ON TASK.TASK_KEY=TT.TASK_KEY
# MAGIC
# MAGIC WHERE 
# MAGIC TT.CURRENT_FLAG = 'Y' 
# MAGIC AND TRANTCURRENT.TASK_TRANSACTION_TYPE_DESCRIPTION NOT IN ('COMPLETED','CANCELLED')
# MAGIC OR
# MAGIC TT.CURRENT_FLAG = 'Y' 
# MAGIC AND DATEDIFF(MONTH,DATE_FORMAT(TT.DATE_COMPLETED,'yyyy-MM-dd'),DATE_FORMAT(CURRENT_DATE(),'yyyy-MM-dd'))<=3
# MAGIC
# MAGIC )
# MAGIC
