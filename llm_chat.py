from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from audio import generate_audio_from_text

# -------------------------
# Initialize LLM with API key
# -------------------------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key="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"
)

# -------------------------
# Prompt template
# -------------------------
prompt = ChatPromptTemplate.from_template(
"""
You are a friendly NCERT teacher for Class 9–10 students.

Step 1: Detect the language style used by the student.

Language rules:
- Tamil words in English letters → Tanglish

Step 2: Reply in the SAME language style.

Use simple explanations with examples.

Question:
{question}

Explain clearly.
"""
)

# -------------------------
# Output parser
# -------------------------
parser = StrOutputParser()

# -------------------------
# LLM pipeline
# -------------------------
chain = prompt | llm | parser

# -------------------------
# Example test question
# -------------------------
if __name__ == "__main__":
    response = chain.invoke({
        "question": "muje capacitor vyaakhya karana"
    })

    audio_file = generate_audio_from_text(response)

    print("Response:", response)
    print("Audio saved at:", audio_file)