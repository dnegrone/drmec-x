# pages/2_⚙️_Admin.py
import streamlit as st
import os
import shutil # Para operações de arquivo, como exclusão
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma

# --- Configurações (MESMAS DO SEU PROJETO) ---
PDF_DIR = "source-pdfs" # Pasta onde os PDFs serão armazenados (pode mudar conforme necessário)
CHROMA_DB_PATH = "./chroma_db"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2" # Mesmo modelo de embedding

st.set_page_config(page_title="Admin | Farmácia Genial ⚙️", page_icon="⚙️")

st.title("Área Administrativa ⚙️")
st.markdown("Gerencie os documentos PDF da sua base de conhecimento.")

# --- Funções de Ajuda ---

# Para garantir que a pasta de PDFs exista
if not os.path.exists(PDF_DIR):
    os.makedirs(PDF_DIR)

# Função para indexar documentos (do seu script indexar_documentos.py)
@st.spinner("Indexando documentos... Isso pode levar um tempo.")
def indexar_documentos(reset_db=False):
    if reset_db:
        if os.path.exists(CHROMA_DB_PATH):
            st.info("Reiniciando a base de conhecimento (excluindo dados antigos)...")
            try:
                shutil.rmtree(CHROMA_DB_PATH)
                st.success("Base de conhecimento antiga excluída.")
            except Exception as e:
                st.error(f"Erro ao excluir a base de conhecimento antiga: {e}")
                return
        # Garante que a pasta chroma_db seja recriada para o persistir
        if not os.path.exists(CHROMA_DB_PATH):
            os.makedirs(CHROMA_DB_PATH)

    documentos = []
    for filename in os.listdir(PDF_DIR):
        if filename.endswith(".pdf"):
            filepath = os.path.join(PDF_DIR, filename)
            try:
                loader = PyPDFLoader(filepath)
                documentos.extend(loader.load())
            except Exception as e:
                st.warning(f"Não foi possível carregar o PDF: {filename}. Erro: {e}")
                continue

    if not documentos:
        st.warning("Nenhum documento PDF válido encontrado para indexar. Adicione PDFs na pasta para iniciar.")
        # Garante que a DB é criada mesmo que vazia, para evitar erros no QA
        embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        db = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
        db.persist()
        return

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documentos)
    
    embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    
    # Cria/atualiza o DB
    db = Chroma.from_documents(
        chunks, embeddings, persist_directory=CHROMA_DB_PATH
    )
    db.persist()
    st.success(f"Base de conhecimento atualizada com {len(chunks)} pedaços de texto!")

# --- Carregamento de PDFs e Visualização ---
st.subheader("Carregar e Visualizar PDFs")
    
uploaded_files = st.file_uploader(
    "Arraste e solte seus arquivos PDF aqui ou clique para selecionar (múltiplos arquivos permitidos)",
    type="pdf",
    accept_multiple_files=True,
    key="pdf_uploader" # Chave adicionada aqui
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join(PDF_DIR, uploaded_file.name)
        if os.path.exists(file_path):
            st.warning(f"O arquivo '{uploaded_file.name}' já existe e será substituído.")
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Arquivo '{uploaded_file.name}' carregado para a pasta.")
    
    # Invalida o cache para recarregar a lista de arquivos após upload
    st.cache_data.clear() # Limpa todo o cache de dados
    st.rerun() # Força o Streamlit a recarregar a página para mostrar os novos arquivos


st.subheader("PDFs Carregados no Sistema")

# Cache para não listar os arquivos toda hora
@st.cache_data(ttl=300) # Cache por 5 minutos, pode ajustar o tempo
def get_files_in_dir(directory):
    return [f for f in os.listdir(directory) if f.endswith(".pdf")]

get_files_in_dir.clear()
files_in_dir = get_files_in_dir(PDF_DIR)

if not files_in_dir:
    st.info("Nenhum PDF encontrado na pasta do sistema. Por favor, carregue um arquivo.")
else:
    # Exibição dos PDFs e botão de exclusão
    for file_name in files_in_dir:
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            st.write(file_name)
        with col2:
            # Chave única para cada botão de exclusão
            if st.button("Excluir", key=f"delete_pdf_{file_name}"):
                file_path_to_delete = os.path.join(PDF_DIR, file_name)
                st.write(f"Tentando excluir: '{file_path_to_delete}'?")
                print(f"DEBUG: Tentando excluir: '{file_path_to_delete}'")
                try:
                    os.remove(file_path_to_delete)
                    st.success(f"'{file_name}' excluído com sucesso!")
                    get_files_in_dir.clear() # Limpa o cache da função get_files_in_dir
                    st.rerun() # Recarrega a página para atualizar a lista
                except Exception as e:
                    st.error(f"Erro ao excluir '{file_name}': {e}")
                    st.exception(e) #detalhes do erro
    
st.markdown("---")

# --- Ações de Treinamento ---
st.subheader("Ações da Base de Conhecimento")

col_retrain, col_reset = st.columns(2)

with col_retrain:
    # Chave única para o botão de retreino
    if st.button("Treinar Sistema com Dados Atuais", help="Adiciona novos dados ou atualiza a base com os PDFs que estão na pasta.", key="btn_retrain_system"):
        indexar_documentos(reset_db=False)
        st.success("Sistema treinado com sucesso! (Dados existentes preservados)")

with col_reset:
    # Aprimoramento da lógica para o botão "Reiniciar TODO o Conhecimento do Sistema"
    if st.button("Reiniciar TODO o Conhecimento do Sistema", help="ATENÇÃO: Exclui todo o conhecimento anterior e reconstrói a base do zero com os PDFs atuais.", type="secondary", key="btn_reset_knowledge"):
        st.session_state['confirm_reset_active'] = True # Ativa o estado de confirmação

    # Só mostra o checkbox se o botão "Reiniciar" foi clicado
    if st.session_state.get('confirm_reset_active', False):
        st.warning("Tem certeza? Esta ação apagará todo o conhecimento atual do sistema!")
        col_confirm, col_cancel = st.columns(2)
        with col_confirm:
            if st.button("Sim, Reiniciar", key="btn_confirm_reset"):
                indexar_documentos(reset_db=True)
                st.success("Conhecimento do sistema reiniciado e treinado com sucesso!")
                st.session_state['confirm_reset_active'] = False # Desativa o estado de confirmação
                st.rerun() # Recarrega para limpar os botões de confirmação
        with col_cancel:
            if st.button("Cancelar", key="btn_cancel_reset"):
                st.info("Reinício cancelado.")
                st.session_state['confirm_reset_active'] = False # Desativa o estado de confirmação
                st.rerun() # Recarrega para limpar os botões de confirmação

st.markdown("---")
st.info("Após carregar novos PDFs, excluí-los ou reiniciar, lembre-se de 'Treinar o Sistema' para que as alterações entrem em vigor na base de conhecimento.")