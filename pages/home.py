# app.py
import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
import os

# --- Configurações (MESMAS DO SEU PROJETO) ---
CHROMA_DB_PATH = "./chroma_db"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
LLM_MODEL_NAME = "llama3" # Ou mistral, phi3, etc. - o modelo que você baixou no Ollama

# --- Função para Carregar a Cadeia RAG (com cache para otimizar) ---
@st.cache_resource
def load_rag_chain():
    # Verifica se a base de dados ChromaDB existe
    if not os.path.exists(CHROMA_DB_PATH):
        st.error(f"Erro: Base de dados ChromaDB não encontrada em '{CHROMA_DB_PATH}'.")
        st.error("Por favor, execute o script 'indexar_documentos.py' primeiro para criar a base de conhecimento.")
        st.stop() # Interrompe a execução do Streamlit

    # Carregar o modelo de embedding
    with st.spinner(f"Carregando modelo de embedding: {EMBEDDING_MODEL_NAME}..."):
        embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    
    # Carregar o ChromaDB persistente
    with st.spinner(f"Carregando base de dados ChromaDB de: {CHROMA_DB_PATH}..."):
        db = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
    
    # Configurar a LLM do Ollama
    with st.spinner(f"Conectando à LLM local: {LLM_MODEL_NAME} (via Ollama)..."):
        # Certifique-se que o aplicativo Ollama está rodando e o modelo LLM_MODEL_NAME foi baixado.
        llm = Ollama(model=LLM_MODEL_NAME)
    
    # Criar a cadeia de RetrievalQA
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(search_kwargs={"k": 4}), # Recupera os 4 chunks mais relevantes
        return_source_documents=True
    )
    return qa_chain

# --- Interface do Streamlit ---
st.set_page_config(page_title="Dr. Mec X - Farmácia Genial 💊", page_icon="💡")

st.title("Dr. Mec X - Farmácia Genial 💊")
st.markdown("Bem-vindo(a) ao seu assistente de conhecimento farmacêutico local!")
st.markdown("Faça perguntas sobre os seus documentos PDF e obtenha respostas baseadas neles.")

# Carregar a cadeia RAG apenas uma vez ao iniciar o aplicativo
qa_chain = load_rag_chain()

# Campo de entrada para a pergunta
user_query = st.text_area("Digite sua pergunta aqui:", placeholder="Ex: Qual a dosagem recomendada para Ibuprofeno em adultos?", height=100)

if st.button("Obter Resposta"):
    if user_query:
        # Exibe um spinner enquanto a resposta está sendo gerada
        with st.spinner("Buscando informações e gerando resposta..."):
            try:
                # Chama a cadeia RAG com a pergunta do usuário
                response = qa_chain.invoke({"query": user_query})
                
                # Exibe a resposta
                st.subheader("Resposta:")
                st.info(response["result"]) # Usa st.info para um fundo azul claro

                # Exibe as fontes, se disponíveis
                if "source_documents" in response and response["source_documents"]:
                    st.subheader("Fontes Encontradas:")
                    for i, doc in enumerate(response["source_documents"]):
                        source_page = doc.metadata.get('page')
                        source_file = doc.metadata.get('source')
                        
                        file_info = os.path.basename(source_file) if source_file else "Desconhecido"
                        page_info = f", Página: {source_page + 1}" if source_page is not None else ""
                        
                        st.markdown(f"- **{i+1}. Arquivo:** `{file_info}`{page_info}")
                else:
                    st.markdown("Nenhuma fonte específica encontrada para esta resposta.")
            except Exception as e:
                st.error(f"Ocorreu um erro ao processar sua pergunta: {e}")
                st.warning("Verifique se o aplicativo Ollama está rodando e se o modelo LLM está disponível.")
    else:
        st.warning("Por favor, digite uma pergunta antes de clicar em 'Obter Resposta'.")

st.markdown("---")
st.markdown("Lembre-se de que a qualidade da resposta depende dos documentos fornecidos e do modelo LLM.")