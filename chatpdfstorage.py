import os
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Directory to store uploaded PDFs
PDF_DIR = "uploaded_pdfs"
os.makedirs(PDF_DIR, exist_ok=True)

def save_uploaded_files(uploaded_files):
    saved_paths = []
    for uploaded_file in uploaded_files:
        # Create a file path in the PDF directory
        file_path = os.path.join(PDF_DIR, uploaded_file.name)
        # Write the uploaded file to the file system
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        saved_paths.append(file_path)
    return saved_paths

def get_pdf_text(pdf_paths):
    text = ""
    for pdf_path in pdf_paths:
        pdf_reader = PdfReader(pdf_path)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def list_stored_pdfs():
    return [f for f in os.listdir(PDF_DIR) if os.path.isfile(os.path.join(PDF_DIR, f))]


def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


def get_conversational_chain():

    prompt_template = """
    Act as AI-PDF expert. Users upload one or more PDF files and ask you questions based on those uploaded files.
    Your job is to understand the question and generate as detailed as possible answers based on the context of PDF. 
    Identify one or more paragraphs that contain relevant information and combine them to provide a long and detailed answer.
    If the answer is not in provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=0.3)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain



def user_input(user_question):
    # Append "explain in detail" to the user's question
    detailed_question = user_question + " Explain in detail."
    
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    new_db = FAISS.load_local("faiss_index", embeddings)
    docs = new_db.similarity_search(detailed_question)

    chain = get_conversational_chain()

    
    response = chain(
        {"input_documents":docs, "question": detailed_question}
        , return_only_outputs=True)

    print(response)
    st.write("Reply: ", response["output_text"])

def main():
    st.set_page_config("Chat PDF")
    st.header("Chat with any PDF")

    user_question = st.text_input("Ask a Question from the PDF Files")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        uploaded_files = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                pdf_paths = save_uploaded_files(uploaded_files)
                raw_text = get_pdf_text(pdf_paths)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")

        # Display the list of stored PDFs
        st.write("Stored PDFs:")
        for pdf_file in list_stored_pdfs():
            st.write(pdf_file)

if __name__ == "__main__":
    main()