# Databricks notebook source
# MAGIC %md
# MAGIC # Load PDF Insight Extractor Documents
# MAGIC
# MAGIC This notebook loads processed PDF document records exported from the local FastAPI backend.
# MAGIC
# MAGIC Expected input file:
# MAGIC
# MAGIC ```text
# MAGIC documents_for_databricks.jsonl
# MAGIC ```
# MAGIC
# MAGIC Each line should contain one JSON document with:
# MAGIC
# MAGIC - file_id
# MAGIC - original_filename
# MAGIC - page_count
# MAGIC - character_count
# MAGIC - processed_at
# MAGIC - text

# COMMAND ----------

import json
from pathlib import Path

# COMMAND ----------

input_path = Path("documents_for_databricks.jsonl")

if not input_path.exists():
    raise FileNotFoundError(
        "Could not find documents_for_databricks.jsonl. "
        "Upload it to the same Databricks workspace folder as this notebook."
    )

records = []

with input_path.open("r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()

        if line:
            records.append(json.loads(line))

print(f"Loaded {len(records)} document records.")

# COMMAND ----------

if not records:
    raise ValueError("No document records were found in the export file.")

documents_df = spark.createDataFrame(records)

display(documents_df)

# COMMAND ----------

documents_df.createOrReplaceTempView("pdf_insight_documents_temp")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   file_id,
# MAGIC   original_filename,
# MAGIC   page_count,
# MAGIC   character_count,
# MAGIC   processed_at
# MAGIC FROM pdf_insight_documents_temp
# MAGIC ORDER BY processed_at DESC

# COMMAND ----------

documents_df.write.mode("overwrite").saveAsTable("pdf_insight_documents")

print("Saved table: pdf_insight_documents")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Validation Queries
# MAGIC
# MAGIC These queries confirm that the document table was created correctly.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS document_count
# MAGIC FROM pdf_insight_documents;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   file_id,
# MAGIC   original_filename,
# MAGIC   page_count,
# MAGIC   character_count,
# MAGIC   processed_at
# MAGIC FROM pdf_insight_documents
# MAGIC ORDER BY processed_at DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   original_filename,
# MAGIC   LEFT(text, 500) AS text_preview
# MAGIC FROM pdf_insight_documents
# MAGIC LIMIT 5;
