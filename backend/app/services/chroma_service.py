import chromadb

client = chromadb.Client()

collection = client.get_or_create_collection(
    name="pdf_documents"
)


def store_embeddings(chunks, embeddings):

    for index, chunk in enumerate(chunks):

        collection.add(
            documents=[chunk],
            embeddings=[embeddings[index]],
            ids=[str(index)]
        )


def search_similar_chunks(query_embedding, top_k=3):

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results["documents"][0]