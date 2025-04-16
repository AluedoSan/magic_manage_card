import streamlit as st
import pandas as pd
import base64
import io
import zipfile
from card_manager import CardManager
from ui_components import (
    render_sidebar,
    render_header,
    render_add_card_form,
    render_view_cards,
    render_search_cards,
    render_stats_dashboard,
    render_export_import
)

# Configuração da página
st.set_page_config(
    page_title="Magic Card Manager",
    page_icon="🧙‍♂️",
    layout="wide"
)

# Inicialização do gerenciador de cartas
@st.cache_resource
def get_card_manager():
    return CardManager()

card_manager = get_card_manager()

# Renderizar cabeçalho
render_header()

# Renderizar barra lateral com menu de navegação
selected_option = render_sidebar()

# Conteúdo principal baseado na opção selecionada
if selected_option == "Adicionar Carta":
    render_add_card_form(card_manager)
    
elif selected_option == "Visualizar Coleção":
    render_view_cards(card_manager)
    
elif selected_option == "Buscar Cartas":
    render_search_cards(card_manager)
    
elif selected_option == "Estatísticas":
    render_stats_dashboard(card_manager)
    
elif selected_option == "Exportar/Importar":
    render_export_import(card_manager)
    
elif selected_option == "Download do Projeto":
    st.header("Download do Projeto")
    
    # Criando arquivo zip com o código fonte
    def create_zip_file():
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            files_to_include = {
                "app.py": open("app.py", "r").read(),
                "card_manager.py": open("card_manager.py", "r").read(),
                "ui_components.py": open("ui_components.py", "r").read(),
                "card_utils.py": open("card_utils.py", "r").read(),
                "requirements.txt": "streamlit==1.22.0\npandas==1.5.3\nmatplotlib==3.7.1\npillow==9.4.0\n",
                "README.md": "# Magic Card Manager\n\nGerenciador de cartas de Magic: The Gathering construído com Streamlit.\n\n## Instalação\n\n```\npip install -r requirements.txt\n```\n\n## Execução\n\n```\nstreamlit run app.py\n```"
            }
            
            for filename, content in files_to_include.items():
                zipf.writestr(filename, content)
        
        return zip_buffer.getvalue()
    
    zip_data = create_zip_file()
    
    # Botão para download
    st.download_button(
        label="Baixar Código Fonte",
        data=zip_data,
        file_name="mtg_card_manager.zip",
        mime="application/zip",
        help="Baixe todos os arquivos de código fonte do projeto"
    )
    
    st.success("O arquivo ZIP contém todos os arquivos necessários para executar o aplicativo.")
    
    st.markdown("""
    ### Instruções para executar o projeto:
    
    1. Descompacte o arquivo ZIP
    2. Instale as dependências: `pip install -r requirements.txt`
    3. Execute o aplicativo: `streamlit run app.py`
    
    O aplicativo será aberto automaticamente no seu navegador padrão.
    """)