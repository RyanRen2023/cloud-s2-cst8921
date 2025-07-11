# Step 1: Install required packages via pip (only need to run once in terminal)
# pip install azure-search-documents langchain openai pypdf tiktoken unstructured langchain-openai

# Step 2: Import required libraries
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain_openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import os

# Step 3: Configure Azure Cognitive Search Client
endpoint = "https://ai-search-xr.search.windows.net"
key = ""
index_name = "index-search"

credential = AzureKeyCredential(key)
client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)

# Step 4: Configure Azure OpenAI LLM
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2023-05-15"
os.environ["OPENAI_API_KEY"] = ""
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://openai-service-xr.openai.azure.com/"

llm = AzureOpenAI(
    deployment_name="gpt-35-turbo-instruct",
    model="gpt-3.5-turbo-instruct",
    temperature=1
)

# Step 5: Load and process PDF data
pdf_path = "demo_paper.pdf"  # Make sure the PDF is in your working directory
loader = PyPDFLoader(pdf_path, extract_images=False)
documents = loader.load_and_split()

# Step 6: Split data into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=5000,
    chunk_overlap=20,
    length_function=len
)
chunks = text_splitter.split_documents(documents)

# Step 7: Upload chunks to Azure Cognitive Search
for index, chunk in enumerate(chunks):
    doc = {
        "id": str(index + 1),
        "data": chunk.page_content,
        "source": chunk.metadata["source"]
    }
    result = client.upload_documents(documents=[doc])

# Step 8: Define RAG response generator
def generate_response(user_question):
    context = ""
    results = client.search(search_text=user_question, top=2)
    for doc in results:
        context += "\n" + doc['data']

    prompt = f"""You will be provided with the question and a related context, you need to answer the question using the context.

Context:
{context}

Question:
{user_question}

Make sure to answer the question only using the context provided. If the context doesn't contain the answer then return "I don't have enough information to answer the question".

Answer:"""

    response = llm(prompt)
    return response

# Step 9: Ask a question
if __name__ == "__main__":
    print("Welcome to the PDF RAG system!  ")
    print("--------------------------------")
    i = 0
    while True:
        print("Please enter your question: (type 'exit' to quit)")    
        user_question = input()
        if user_question == "exit":
            break
        i += 1
        print(f"Question {i}: ", user_question)
        answer = generate_response(user_question)
        print(f"Answer {i}: ", answer)
        print("--------------------------------")

