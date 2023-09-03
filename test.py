import chromadb

chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="Rand-db")

collection.add(
    documents=["data"],
        # metadatas=metadatas,
        ids=["id1"]
    )
results = collection.query(
    query_texts=["data"],
    n_results=3
)

print(results)
