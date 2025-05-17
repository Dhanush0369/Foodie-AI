import os   
import streamlit as st
from langchain_huggingface import HuggingFaceEndpoint, HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

DB_FAISS_PATH = "vectorstore/db_faiss"

@st.cache_resource
def get_vectorstore():
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
    return db

def load_llm(huggingface_repo_id, HF_TOKEN):
    return HuggingFaceEndpoint(
        endpoint_url=f"https://api-inference.huggingface.co/models/{huggingface_repo_id}",
        task="text-generation",
        temperature=0.5,
        huggingfacehub_api_token=HF_TOKEN,
    )

def set_custom_prompt(custom_prompt_template):
    prompt = PromptTemplate(template=custom_prompt_template, input_variables=["context", "input"])
    return prompt

def main():
    st.title("Ask Foodie.AI!")

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    prompt = st.chat_input("Enter your question here")

    if prompt:
        with st.chat_message('user'):
            st.markdown(prompt)
        st.session_state.messages.append({'role': 'user', 'content': prompt})

        HF_TOKEN = os.environ.get("HF_TOKEN")
        if not HF_TOKEN:
            st.error("HuggingFace API token not found. Please set the HF_TOKEN environment variable.")
            return

        HUGGINGFACE_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.3"

        CUSTOM_PROMPT_TEMPLATE = """
        You are an expert assistant who only has information about three restaurants: Heritage, SardaarJi, and THAI PAVILION.

        Use only the information provided in the context below to answer the user's question related to menu,location and phone number.
        If the answer cannot be found in the context, simply reply:
        "I'm sorry, I don't have that information."

        Do not guess, invent information, or mention any other restaurants.
        Keep your answer brief and direct.

        Context:
        {context}

        User question:
        {input}
        
        Your answer:
        """

        try:
            with st.spinner("Thinking..."):
                llm = load_llm(huggingface_repo_id=HUGGINGFACE_REPO_ID, HF_TOKEN=HF_TOKEN)
                retriever = get_vectorstore().as_retriever(search_kwargs={'k': 5})

                docs = retriever.get_relevant_documents(prompt)
                print("DEBUG: Retrieved docs:", docs)
                if not docs:
                    st.error("No relevant documents found for your query.")
                    return

                prompt_template = set_custom_prompt(CUSTOM_PROMPT_TEMPLATE)
                combine_docs_chain = create_stuff_documents_chain(llm, prompt_template)
                qa_chain = create_retrieval_chain(retriever, combine_docs_chain)

                response = qa_chain.invoke({"input": prompt})
                print("DEBUG: Chain response:", response)

                result = response["answer"].split("Answer:")[-1].strip()

            with st.chat_message('assistant'):
                st.markdown(result)
            st.session_state.messages.append({'role': 'assistant', 'content': result})

        except Exception as e:
            print("Full exception:", repr(e))
            st.error(f"Error: {str(e)}")



if __name__ == "__main__":
    main()
