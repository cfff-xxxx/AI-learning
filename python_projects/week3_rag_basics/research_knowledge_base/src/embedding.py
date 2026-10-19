from langchain_community.embeddings import HuggingFaceEmbeddings


def get_embedding_model():
    model=HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-zh-v1.5"
    )
    return model

if __name__ == "__main__":
    model = get_embedding_model()
    text = "Agent轻量化研究"
    vector = model.embed_query(text)

    print(len(vector))
    print(vector[:10])