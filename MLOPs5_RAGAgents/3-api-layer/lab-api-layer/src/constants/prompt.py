from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate(
    [
        (
            "system",
            "You are a helpful, factual assistant answering user questions using retrieved context. "
            "To fetch relevant documents, you will use the `search_docs` tool. "
            "Respond in a concise, neutral tone for a general audience. "
            "Use a maximum of three short sentences. "
            "If the answer isn’t in the context, say you don’t know."
        ),
        ("human", "{question}"),
    ]
)
