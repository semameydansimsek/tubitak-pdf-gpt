import streamlit as st
import pdfplumber
import openai

# OpenAI API key input (from sidebar)
openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

# App title
st.title("TÜBİTAK PDF Question-Answer Assistant")

# Upload PDF file
uploaded_pdf = st.file_uploader("Upload the TÜBİTAK PDF file", type="pdf")

# Enter user question
question = st.text_input("Ask your question:")

# Extract text from PDF
def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# Generate GPT response
def generate_gpt_answer(api_key, question, pdf_text):
    client = openai.OpenAI(api_key=api_key)

    prompt = f"""
Below is an excerpt from the TÜBİTAK Project Guide. The user asked:
\"{question}\"

Based on the content, give a helpful, formal answer:
\"\"\"{pdf_text[:3000]}\"\"\"
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    return response.choices[0].message.content

# When button is clicked
if st.button("Generate Answer"):
    if not uploaded_pdf:
        st.warning("Please upload a PDF file first.")
    elif not question.strip():
        st.warning("Please enter a question.")
    elif not openai_api_key:
        st.warning("Please enter your OpenAI API Key.")
    else:
        with st.spinner("Generating answer with GPT..."):
            pdf_content = extract_text_from_pdf(uploaded_pdf)
            answer = generate_gpt_answer(openai_api_key, question, pdf_content)
            st.success("Answer generated!")
            st.write("### GPT's Response:")
            st.write(answer)
