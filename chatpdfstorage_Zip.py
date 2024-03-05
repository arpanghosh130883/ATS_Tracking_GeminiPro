import os
import zipfile
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

# Load environment variables and configure the API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Directory to store uploaded PDFs
PDF_DIR = "uploaded_pdfs"
os.makedirs(PDF_DIR, exist_ok=True)

def extract_pdfs_from_zip(zip_file_path):
    """Extracts PDF files from a ZIP file and saves them to the PDF directory."""
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(PDF_DIR)
    return [os.path.join(PDF_DIR, f) for f in os.listdir(PDF_DIR) if f.lower().endswith('.pdf')]

def get_pdf_text(pdf_paths):
    """Extracts text from the given PDF paths."""
    text = ""
    for pdf_path in pdf_paths:
        pdf_reader = PdfReader(pdf_path)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def list_stored_pdfs():
    """Lists PDF files stored in the PDF directory."""
    return [f for f in os.listdir(PDF_DIR) if os.path.isfile(os.path.join(PDF_DIR, f)) and f.endswith('.pdf') and not f.endswith('.zip')]

def get_text_chunks(text):
    """Splits text into chunks for processing."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    return text_splitter.split_text(text)

def get_vector_store(text_chunks):
    """Creates and saves a vector store from text chunks."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    """Creates and returns a conversational chain for the chatbot."""
    prompt_template = """
    Act as AI-PDF expert. Users upload one or more PDF files and ask you questions based on those uploaded files.
    Your job is to understand the question and generate as detailed as possible answers based on the context of PDF. 
    Identify one or more paragraphs that contain relevant information and combine them to provide a long and detailed answer.
    If the answer is not in provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    return load_qa_chain(model, chain_type="stuff", prompt=prompt)

def user_input(user_question):
    """Processes the user's question and displays the response."""
    detailed_question = user_question + " Explain in detail."
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings)
    docs = new_db.similarity_search(detailed_question)
    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": detailed_question}, return_only_outputs=True)
    st.write("Reply:", response["output_text"])

def main():
    """Main function to run the Streamlit app."""
    st.set_page_config("Chat PDF")

    # Custom CSS for black background
    st.markdown(
        """
        <style>
        body {
            background-color: black;
            color: white;
        }
        .stTextInput>div>div>input {
            background-color: #333;
            color: white;
        }
        .stButton>button {
            border: 2px solid #4CAF50;
            background-color: #333;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Chat with Your PDFs")

    with st.sidebar:
        st.header("Upload PDFs")
        uploaded_zip = st.file_uploader("Upload a ZIP file containing PDFs", type="zip")
        if st.button("Process Uploaded ZIP"):
            with st.spinner("Processing..."):
                if uploaded_zip is not None:
                    zip_path = os.path.join(PDF_DIR, uploaded_zip.name)
                    with open(zip_path, "wb") as f:
                        f.write(uploaded_zip.getbuffer())
                    pdf_paths = extract_pdfs_from_zip(zip_path)
                    raw_text = get_pdf_text(pdf_paths)
                    text_chunks = get_text_chunks(raw_text)
                    get_vector_store(text_chunks)
                    st.success("PDFs processed successfully!")
        
        # Display the list of stored PDFs
        st.header("Stored PDFs")
        for pdf_file in list_stored_pdfs():
            st.text(pdf_file)

    st.header("Ask a Question")
    user_question = st.text_input("Enter your question here:")
    if user_question:
        user_input(user_question)

if __name__ == "__main__":
    main()
