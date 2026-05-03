# Databricks notebook source
# MAGIC %md
# MAGIC # Search Document Chunks
# MAGIC
# MAGIC This notebook performs a simple keyword search over the `pdf_insight_document_chunks` table.
# MAGIC
# MAGIC This is a baseline retrieval step before adding AI search or agent behavior.

# COMMAND ----------

import re

from pyspark.sql.functions import col, lit, lower, when

# COMMAND ----------

dbutils.widgets.text("search_query", "experience")
search_query = dbutils.widgets.get("search_query").strip()

if not search_query:
    raise ValueError("search_query cannot be empty.")

print(f"Search query: {search_query}")

# COMMAND ----------

chunks_df = spark.table("pdf_insight_document_chunks")

display(chunks_df.limit(5))

# COMMAND ----------

search_terms = re.findall(r"\b[a-zA-Z0-9][a-zA-Z0-9+#.-]*\b", search_query.lower())

if not search_terms:
    raise ValueError("No searchable terms were found in the query.")

print(f"Search terms: {search_terms}")

# COMMAND ----------

chunk_text_lower = lower(col("chunk_text"))
score_expression = lit(0)

for term in search_terms:
    score_expression = score_expression + when(
        chunk_text_lower.contains(term),
        lit(1),
    ).otherwise(lit(0))

results_df = (
    chunks_df
    .withColumn("match_score", score_expression)
    .where(col("match_score") > 0)
    .orderBy(
        col("match_score").desc(),
        col("original_filename"),
        col("chunk_index"),
    )
)

display(
    results_df.select(
        "match_score",
        "original_filename",
        "chunk_index",
        "chunk_id",
        "chunk_text",
    )
)

# COMMAND ----------

results_df.createOrReplaceTempView("pdf_insight_search_results")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   match_score,
# MAGIC   original_filename,
# MAGIC   chunk_index,
# MAGIC   LEFT(chunk_text, 500) AS chunk_preview
# MAGIC FROM pdf_insight_search_results
# MAGIC ORDER BY match_score DESC, original_filename, chunk_index
# MAGIC LIMIT 10;
