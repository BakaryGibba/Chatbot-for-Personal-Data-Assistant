import os
import torch
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.llms import HuggingFaceHub

# Check for GPU availability and set the appropriate device for computation.
DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"

# Global variables
conversation_retrieval_chain = None
chat_history = []
llm_hub = None
embeddings = None

# Function to initialize the language model and its embeddings
def init_llm():
    global llm_hub, embeddings
    # Set up the environment variable for HuggingFace and initialize the desired model.
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

    try:
        # repo name for the model
        model_id = "tiiuae/falcon-7b-instruct"
        # load the model into the HuggingFaceHub
        llm_hub = HuggingFaceHub(repo_id=model_id, model_kwargs={"temperature": 0.1, "max_new_tokens": 600, "max_length": 600})
        print("Language model initialized successfully.")
        
        # Initialize embeddings using a pre-trained model to represent the text data.
        embeddings = HuggingFaceInstructEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={"device": DEVICE}
        )
        print("Embeddings initialized successfully.")
    except Exception as e:
        print(f"Error initializing language model or embeddings: {e}")
        raise

# Function to process a PDF document
def process_document(document_path):
    global conversation_retrieval_chain

    print(f"Processing document: {document_path}")

    try:
        # Load the document
        loader = PyPDFLoader(document_path)
        documents = loader.load()
        print("Document loaded successfully.")

        # Split the document into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=64)
        texts = text_splitter.split_documents(documents)
        print("Document split into chunks.")

        # Create an embeddings database using Chroma from the split text chunks.
        db = Chroma.from_documents(texts, embedding=embeddings)
        print("Embeddings created and stored in the database.")

        # Build the QA chain, which utilizes the LLM and retriever for answering questions.
        conversation_retrieval_chain = RetrievalQA.from_chain_type(
            llm=llm_hub,
            chain_type="stuff",
            retriever=db.as_retriever(search_type="mmr", search_kwargs={'k': 6, 'lambda_mult': 0.25}),
            return_source_documents=False,
            input_key="question"
        )
        print("Conversation retrieval chain initialized.")
    
    except Exception as e:
        print(f"Error processing document: {e}")
        raise

# Function to process a user prompt
def process_prompt(prompt):
    global conversation_retrieval_chain
    global chat_history

    if conversation_retrieval_chain is None:
        print("Error: conversation_retrieval_chain is not initialized")
        raise ValueError("conversation_retrieval_chain is not initialized")

    try:
        # Query the model
        output = conversation_retrieval_chain({"question": prompt, "chat_history": chat_history})
        answer = output["result"]

        # Update the chat history
        chat_history.append((prompt, answer))

        # Return the model's response
        return answer
    except Exception as e:
        print(f"Error processing prompt: {e}")
        raise

# Initialize the language model
init_llm()
