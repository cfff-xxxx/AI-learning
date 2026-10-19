def retrieve_documents(
        db,
        query,
        k=5
):
    docs=db.similarity_search(
        query,
        k=k
    )

    return  docs