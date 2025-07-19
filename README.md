# Dr. Mec X - Farmácia Genial: Assistente de Conhecimento Farmacêutico 💊💡

## 📖 Sobre o Projeto

O Farmácia Genial é um assistente inteligente baseado em Large Language Models (LLMs) e Retrieval Augmented Generation (RAG). Ele permite que profissionais e estudantes da área farmacêutica consultem e obtenham respostas precisas a partir de uma base de conhecimento personalizada, construída com documentos PDF específicos (por exemplo, bulas, artigos científicos, diretrizes, etc.).

O objetivo é centralizar e facilitar o acesso à informação crucial, transformando documentos extensos em uma fonte interativa de conhecimento.

### ✨ Funcionalidades

- Upload de PDFs: Carregue seus próprios documentos PDF para construir sua base de conhecimento.
- Gestão de Documentos: Visualize os PDFs carregados e remova-os da base do sistema.
- Treinamento da Base de Conhecimento: Indexe os documentos PDF para que a LLM possa consultá-los.
- Reinício Completo da Base: Opção para apagar e reconstruir toda a base de conhecimento do zero.
- Perguntas e Respostas: Faça perguntas em linguagem natural e receba respostas baseadas exclusivamente no conteúdo dos PDFs carregados.
- Fontes da Resposta: Visualização dos documentos e páginas utilizadas para gerar a resposta.

### 🛠️ Tecnologias Utilizadas

- Python: Linguagem principal de desenvolvimento.
- Streamlit: Framework para criação rápida da interface web interativa.
- Ollama: Para rodar Large Language Models (LLMs) localmente (ex: Llama3).
- LangChain: Framework para desenvolvimento de aplicações com LLMs, facilitando a orquestração do RAG.
- ChromaDB: Base de dados vetorial para armazenar os embeddings dos documentos e realizar a busca de similaridade.
- Sentence Transformers: Para gerar os embeddings (representações vetoriais) dos textos.
- PyPDFLoader: Para carregar e extrair texto de arquivos PDF.

---

## 🚀 Como Executar o Projeto

Siga os passos abaixo para configurar e rodar o Farmácia Genial em sua máquina local.

### Pré-requisitos

Certifique-se de ter instalado:

- Python 3.9+
- Ollama: Baixe e instale o Ollama em ollama.com.

### 1. Clonar o Repositório

```bash
git clone https://github.com/dnegrone/drmec-x.git
cd drmec-x # Ou o nome da pasta do seu projeto
```

### 2. Configurar o Ambiente Virtual

É altamente recomendável usar um ambiente virtual para gerenciar as dependências do projeto.

```bash
python3 -m venv venv (ou python -m venv venv)
source venv/bin/activate # No Linux/macOS
# venv\Scripts\activate # No Windows
```

### 3. Instalar Dependências

Instale todas as bibliotecas Python necessárias.

```bash
pip install -r requirements.txt
```

Nota: Se você ainda não criou o requirements.txt, pode gerá-lo a partir das suas instalações atuais:
`pip freeze > requirements.txt`

Ou, instale as principais individualmente:
`pip install streamlit ollama langchain langchain-community pypdf sentence-transformers chromadb`

### 4. Baixar o Modelo LLM com Ollama

Abra seu terminal e baixe o modelo LLM que será usado pelo projeto. Recomendamos llama3 para começar.

```bash
ollama run llama3
```

Espere o download ser concluído e o modelo inicializar. Você pode fechar o terminal do Ollama depois de garantir que o modelo está baixado, mas o serviço Ollama precisa estar rodando em segundo plano para o projeto funcionar.

### 5. Executar o Aplicativo Streamlit

Com todas as dependências instaladas e o Ollama rodando, inicie o aplicativo.

```bash
streamlit run streamlit_app.py
```

(Se você ainda tem a estrutura de pastas `pages/`, o comando seria `streamlit run streamlit_app.py`)

O aplicativo será aberto automaticamente no seu navegador padrão (geralmente em http://localhost:8501).

---

## ⚙️ Uso da Área Administrativa

### Após iniciar o aplicativo:

1. **Acesse a Área Admin:** Clique no botão **"⚙️ Admin"** na interface para acessar a área de gerenciamento.
2. **Carregar PDFs:** Arraste e solte seus documentos PDF na seção **"Carregar e Visualizar PDFs"**.
3. **Treinar Sistema:** Após carregar os PDFs, clique em **"Treinar Sistema com Dados Atuais"** na seção **"Ações da Base de Conhecimento"** para indexar o conteúdo dos PDFs na base de dados do sistema.
4. **Reiniciar Conhecimento:** Se desejar apagar e reconstruir toda a base de conhecimento, use o botão **"Reiniciar TODO o Conhecimento do Sistema"** (requer confirmação).
5. **Excluir PDFs:** Na lista de **"PDFs Carregados no Sistema"**, você pode clicar em **"Excluir"** ao lado de cada arquivo para removê-lo da pasta. Lembre-se de **"Treinar o Sistema"** novamente após excluir arquivos para que as alterações reflitam na base de conhecimento da IA.

### 🙋 Contribuição

Contribuições são bem-vindas! Se você tiver sugestões, melhorias ou encontrar bugs, sinta-se à vontade para abrir uma issue ou enviar um pull request.

### 📄 Licença

Este projeto está licenciado sob a licença MIT License.

### 📞 Contato

Alexander Costa - https://alexcesar.com
