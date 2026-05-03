# Databricks notebook source
# MAGIC %md
# MAGIC # Chunk PDF Documents
# MAGIC
# MAGIC This notebook reads the `pdf_insight_documents` table and splits each document into smaller text chunks.
# MAGIC
# MAGIC The output table is:
# MAGIC
# MAGIC ```text
# MAGIC pdf_insight_document_chunks
# MAGIC ```

# COMMAND ----------

from pyspark.sql import Row

# COMMAND ----------

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200

# COMMAND ----------

documents_df = spark.table("pdf_insight_documents")

display(documents_df)

# COMMAND ----------

def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - overlap

        if start < 0:
            start = 0

        if start >= len(text):
            break

    return chunks

# COMMAND ----------

chunk_rows = []

for document in documents_df.collect():
    chunks = chunk_text(
        text=document["text"],
        chunk_size=CHUNK_SIZE,
        overlap=CHUNK_OVERLAP,
    )

    for chunk_index, chunk in enumerate(chunks):
        chunk_rows.append(
            Row(
                chunk_id=f"{document['file_id']}_{chunk_index}",
                file_id=document["file_id"],
                original_filename=document["original_filename"],
                chunk_index=chunk_index,
                chunk_text=chunk,
                chunk_character_count=len(chunk),
            )
        )

print(f"Created {len(chunk_rows)} document chunks.")

# COMMAND ----------

if not chunk_rows:
    raise ValueError("No chunks were created. Confirm that pdf_insight_documents contains extracted text.")

chunks_df = spark.createDataFrame(chunk_rows)

display(chunks_df)

# COMMAND ----------

chunks_df.write.mode("overwrite").saveAsTable("pdf_insight_document_chunks")

print("Saved table: pdf_insight_document_chunks")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Validation Queries

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS chunk_count
# MAGIC FROM pdf_insight_document_chunks;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   original_filename,
# MAGIC   COUNT(*) AS chunks_per_document
# MAGIC FROM pdf_insight_document_chunks
# MAGIC GROUP BY original_filename
# MAGIC ORDER BY chunks_per_document DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   chunk_id,
# MAGIC   original_filename,
# MAGIC   chunk_index,
# MAGIC   chunk_character_count,
# MAGIC   LEFT(chunk_text, 500) AS chunk_preview
# MAGIC FROM pdf_insight_document_chunks
# MAGIC ORDER BY original_filename, chunk_index
# MAGIC LIMIT 10;
