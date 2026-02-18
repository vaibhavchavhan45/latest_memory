from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


def summarize_text(text: str) -> str:
    llm = ChatOpenAI(temperature=0.0)

    prompt = PromptTemplate(
        template="""
Summarize the following conversation briefly.
Preserve key facts, decisions, and context.

Conversation:
{conversation}

Summary:
""",
        input_variables=["conversation"],
    )

    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"conversation": text})
