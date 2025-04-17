import streamlit as st
import matplotlib.pyplot as plt
import base64
from card_utils import get_card_image_url, validate_card

def render_header():
    """Renderiza o cabeçalho do aplicativo"""
    st.title("🧙‍♂️ Magic Card Manager")
    st.markdown("Gerencie sua coleção de cartas de Magic: The Gathering")

def render_sidebar():
    """Renderiza a barra lateral com menu de navegação"""
    st.sidebar.title("Menu")
    options = [
        "Adicionar Carta",
        "Visualizar Coleção",
        "Buscar Cartas",
        "Estatísticas",
        "Exportar/Importar",
        "Download do Projeto"
    ]
    selected_option = st.sidebar.radio("Selecione uma opção:", options)
    
    # Informações adicionais
    st.sidebar.markdown("---")
    st.sidebar.info("""
    ### Sobre o App
    Este aplicativo permite gerenciar sua coleção de cartas de Magic: The Gathering.
    
    - Adicione cartas à sua coleção
    - Visualize e edite sua coleção
    - Busque cartas por diferentes critérios
    - Veja estatísticas da sua coleção
    - Exporte e importe dados
    """)
    
    return selected_option

def render_add_card_form(card_manager):
    """Renderiza o formulário para adicionar novas cartas"""
    st.header("Adicionar Carta")
    
    # Formulário para adicionar carta
    with st.form("add_card_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Nome da Carta", key="name")
            edition = st.text_input("Edição", key="edition")
            card_type = st.selectbox(
                "Tipo",
                ["Criatura", "Mágica Instantânea", "Feitiço", "Encantamento", "Artefato", "Planeswalker", "Terra", "Outro"]
            )
            rarity = st.selectbox(
                "Raridade", 
                ["Comum", "Incomum", "Rara", "Mítica", "Especial"]
            )
            colors = st.multiselect(
                "Cores", 
                ["Branco", "Azul", "Preto", "Vermelho", "Verde", "Incolor", "Multicolorido"]
            )
            cmc = st.number_input("Custo de Mana Convertido", min_value=0, step=1)
        
        with col2:
            quantity = st.number_input("Quantidade", min_value=1, step=1, value=1)
            condition = st.selectbox(
                "Condição", 
                ["Mint", "Near Mint", "Excellent", "Good", "Light Played", "Played", "Poor"]
            )
            price_bought = st.number_input("Preço de Compra (R$)", min_value=0.0, step=0.01)
            price_current = st.number_input("Preço Atual (R$)", min_value=0.0, step=0.01)
            foil = st.checkbox("Foil")
            
            # Informação sobre busca de cartas (removido o botão que causava o erro)
            st.info("Integração com API de cartas disponível em versões futuras.")
        
        # Botão de submissão do formulário
        submitted = st.form_submit_button("Adicionar Carta")
        
        if submitted:
            # Validar entradas
            if not name or not edition:
                st.error("Nome e Edição são campos obrigatórios!")
            else:
                # Adicionar carta à coleção
                card_data = {
                    'name': name,
                    'edition': edition,
                    'card_type': card_type,
                    'rarity': rarity,
                    'colors': colors,
                    'cmc': cmc,
                    'quantity': quantity,
                    'condition': condition,
                    'price_bought': price_bought,
                    'price_current': price_current,
                    'foil': foil
                }
                
                # Validar dados da carta
                validation_result = validate_card(card_data)
                if validation_result['valid']:
                    success = card_manager.add_card(card_data)
                    if success:
                        st.success(f"Carta '{name}' adicionada com sucesso!")
                        # Limpar formulário
                        st.rerun()
                else:
                    st.error(f"Erro ao adicionar carta: {validation_result['error']}")

def render_view_cards(card_manager):
    """Renderiza a visualização da coleção"""
    st.header("Visualizar Coleção")
    
    if card_manager.collection.empty:
        st.info("Sua coleção está vazia. Adicione algumas cartas primeiro!")
        return
    
    # Filtros
    st.subheader("Filtros")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_edition = st.selectbox(
            "Filtrar por Edição", 
            ["Todas"] + list(card_manager.collection['edition'].unique())
        )
    
    with col2:
        filter_rarity = st.selectbox(
            "Filtrar por Raridade", 
            ["Todas"] + list(card_manager.collection['rarity'].unique())
        )
    
    with col3:
        filter_type = st.selectbox(
            "Filtrar por Tipo", 
            ["Todos"] + list(card_manager.collection['card_type'].unique())
        )
    
    # Aplicar filtros
    filtered_collection = card_manager.collection.copy()
    if filter_edition != "Todas":
        filtered_collection = filtered_collection[filtered_collection['edition'] == filter_edition]
    if filter_rarity != "Todas":
        filtered_collection = filtered_collection[filtered_collection['rarity'] == filter_rarity]
    if filter_type != "Todos":
        filtered_collection = filtered_collection[filtered_collection['card_type'] == filter_type]
    
    # Exibir coleção
    st.subheader(f"Coleção ({len(filtered_collection)} cartas únicas, {filtered_collection['quantity'].sum()} no total)")
    
    # Opção para exibir/editar cada carta
    for idx, card in filtered_collection.iterrows():
        with st.expander(f"{card['name']} ({card['edition']}) - Qtd: {card['quantity']}"):
            col1, col2 = st.columns([1, 3])
            
            with col1:
                # Tenta mostrar uma imagem da carta (fictícia para este exemplo)
                image_url = get_card_image_url(card['name'], card['edition'])
                st.image(image_url, caption=card['name'], use_container_width=True)
            
            with col2:
                # Exibe detalhes da carta
                st.markdown(f"""
                **Edição:** {card['edition']}  
                **Tipo:** {card['type'] if 'type' in card else card['card_type']}  
                **Raridade:** {card['rarity']}  
                **Cores:** {card['colors']}  
                **CMC:** {card['cmc']}  
                **Condição:** {card['condition']}  
                **Foil:** {'Sim' if card['foil'] else 'Não'}  
                **Valor de Compra:** R$ {card['price_bought']:.2f}  
                **Valor Atual:** R$ {card['price_current']:.2f}  
                **Valor Total:** R$ {card['price_current'] * card['quantity']:.2f}  
                **Data de Adição:** {card['date_added']}
                """)
                
                # Opções para editar ou remover (corrigido para não usar botões dentro de forms)
                edit_col, remove_col = st.columns(2)
                
                with edit_col:
                    # Movido para fora de qualquer form
                    if st.button(f"Editar", key=f"edit_{idx}"):
                        st.session_state['edit_card_idx'] = idx
                        st.session_state['edit_card_data'] = card.to_dict()
                
                with remove_col:
                    # Movido para fora de qualquer form
                    if st.button(f"Remover", key=f"remove_{idx}"):
                        st.session_state[f'show_remove_form_{idx}'] = True
                
                # Exibe formulário de remoção se o botão foi clicado
                if st.session_state.get(f'show_remove_form_{idx}', False):
                    with st.form(key=f"remove_form_{idx}"):
                        remove_qty = st.number_input(
                            "Quantidade a remover:", 
                            min_value=1, 
                            max_value=card['quantity'], 
                            value=1,
                            key=f"remove_qty_{idx}"
                        )
                        confirm_remove = st.form_submit_button("Confirmar Remoção")
                        
                        if confirm_remove:
                            card_manager.remove_card(idx, remove_qty)
                            st.success(f"Removido {remove_qty} unidade(s) de {card['name']}")
                            st.session_state[f'show_remove_form_{idx}'] = False
                            st.rerun()
    
    # Modal de edição
    if 'edit_card_idx' in st.session_state:
        st.subheader("Editar Carta")
        idx = st.session_state['edit_card_idx']
        card_data = st.session_state['edit_card_data']
        
        with st.form("edit_card_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                card_data['name'] = st.text_input("Nome da Carta", value=card_data['name'])
                card_data['edition'] = st.text_input("Edição", value=card_data['edition'])
                card_data['card_type'] = st.selectbox(
                    "Tipo", 
                    ["Criatura", "Mágica Instantânea", "Feitiço", "Encantamento", "Artefato", "Planeswalker", "Terra", "Outro"],
                    index=["Criatura", "Mágica Instantânea", "Feitiço", "Encantamento", "Artefato", "Planeswalker", "Terra", "Outro"].index(card_data['card_type'])
                )
                card_data['rarity'] = st.selectbox(
                    "Raridade", 
                    ["Comum", "Incomum", "Rara", "Mítica", "Especial"],
                    index=["Comum", "Incomum", "Rara", "Mítica", "Especial"].index(card_data['rarity'])
                )
                # Trata cores como uma lista
                colors_list = card_data['colors']
                if isinstance(colors_list, str):
                    colors_list = colors_list.split(',')
                card_data['colors'] = st.multiselect(
                    "Cores", 
                    ["Branco", "Azul", "Preto", "Vermelho", "Verde", "Incolor", "Multicolorido"],
                    default=colors_list
                )
            
            with col2:
                card_data['quantity'] = st.number_input("Quantidade", min_value=1, value=int(card_data['quantity']))
                card_data['condition'] = st.selectbox(
                    "Condição", 
                    ["Mint", "Near Mint", "Excellent", "Good", "Light Played", "Played", "Poor"],
                    index=["Mint", "Near Mint", "Excellent", "Good", "Light Played", "Played", "Poor"].index(card_data['condition'])
                )
                card_data['price_bought'] = st.number_input("Preço de Compra (R$)", min_value=0.0, value=float(card_data['price_bought']))
                card_data['price_current'] = st.number_input("Preço Atual (R$)", min_value=0.0, value=float(card_data['price_current']))
                card_data['foil'] = st.checkbox("Foil", value=bool(card_data['foil']))
            
            # Botões corretos para formulário
            col1, col2 = st.columns(2)
            with col1:
                save_changes = st.form_submit_button("Salvar Alterações")
            with col2:
                cancel = st.form_submit_button("Cancelar")
            
            if save_changes:
                success = card_manager.update_card(idx, card_data)
                if success:
                    st.success(f"Carta '{card_data['name']}' atualizada com sucesso!")
                    del st.session_state['edit_card_idx']
                    del st.session_state['edit_card_data']
                    st.rerun()
            
            if cancel:
                del st.session_state['edit_card_idx']
                del st.session_state['edit_card_data']
                st.rerun()

def render_search_cards(card_manager):
    """Renderiza a funcionalidade de busca de cartas"""
    st.header("Buscar Cartas")
    
    if card_manager.collection.empty:
        st.info("Sua coleção está vazia. Adicione algumas cartas primeiro!")
        return
    
    # Usamos um formulário para a busca
    with st.form("search_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            search_query = st.text_input("Termo de busca")
        
        with col2:
            search_field = st.selectbox(
                "Buscar em",
                ["all", "name", "edition", "card_type", "rarity", "colors"]
            )
        
        search_button = st.form_submit_button("Buscar")
    
    if search_button and search_query:
        results = card_manager.search_cards(search_query, search_field)
        
        if results.empty:
            st.info(f"Nenhuma carta encontrada para '{search_query}'")
        else:
            st.success(f"Encontradas {len(results)} cartas")
            st.dataframe(results)
            
            # Opção para exportar resultados
            csv = results.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="search_results.csv">Baixar resultados da busca (CSV)</a>'
            st.markdown(href, unsafe_allow_html=True)

def render_stats_dashboard(card_manager):
    """Renderiza o painel de estatísticas"""
    st.header("Estatísticas da Coleção")
    
    if card_manager.collection.empty:
        st.info("Sua coleção está vazia. Adicione algumas cartas primeiro!")
        return
    
    stats = card_manager.get_stats()
    
    # Métricas principais
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Cartas", stats['total_cards'])
    
    with col2:
        st.metric("Cartas Únicas", stats['unique_cards'])
    
    with col3:
        st.metric("Valor Total da Coleção", f"R$ {stats['total_value']:.2f}")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Cartas por Cor")
        if stats['cards_by_color']:
            fig, ax = plt.subplots()
            ax.pie(
                stats['cards_by_color'].values(),
                labels=stats['cards_by_color'].keys(),
                autopct='%1.1f%%'
            )
            ax.axis('equal')
            st.pyplot(fig)
        else:
            st.info("Não há dados suficientes para gerar o gráfico")
    
    with col2:
        st.subheader("Cartas por Raridade")
        if stats['cards_by_rarity']:
            fig, ax = plt.subplots()
            ax.bar(
                stats['cards_by_rarity'].keys(),
                stats['cards_by_rarity'].values()
            )
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.info("Não há dados suficientes para gerar o gráfico")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Cartas por Tipo")
        if stats['cards_by_type']:
            fig, ax = plt.subplots()
            ax.pie(
                stats['cards_by_type'].values(),
                labels=stats['cards_by_type'].keys(),
                autopct='%1.1f%%'
            )
            ax.axis('equal')
            st.pyplot(fig)
        else:
            st.info("Não há dados suficientes para gerar o gráfico")
    
    with col2:
        st.subheader("Cartas por Edição")
        # Limitamos a 10 edições para melhor visualização
        top_editions = dict(sorted(stats['cards_by_edition'].items(), key=lambda x: x[1], reverse=True)[:10])
        if top_editions:
            fig, ax = plt.subplots()
            ax.bar(
                top_editions.keys(),
                top_editions.values()
            )
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.info("Não há dados suficientes para gerar o gráfico")
    
    # Estatísticas de valor
    st.subheader("Análise de Valor")
    
    # Calcula o valor médio por carta
    if stats['total_cards'] > 0:
        avg_value = stats['total_value'] / stats['total_cards']
        st.info(f"Valor médio por carta: R$ {avg_value:.2f}")
    
    # Cartas mais valiosas
    st.subheader("Top 10 Cartas Mais Valiosas")
    top_value_cards = card_manager.collection.sort_values(by='price_current', ascending=False).head(10)
    if not top_value_cards.empty:
        st.dataframe(top_value_cards[['name', 'edition', 'rarity', 'price_current', 'quantity']])
    else:
        st.info("Não há dados para mostrar")

def render_export_import(card_manager):
    """Renderiza as opções de exportação e importação"""
    st.header("Exportar/Importar Coleção")
    
    tab1, tab2 = st.tabs(["Exportar", "Importar"])
    
    with tab1:
        st.subheader("Exportar Coleção")
        
        if card_manager.collection.empty:
            st.info("Sua coleção está vazia. Adicione algumas cartas primeiro!")
        else:
            export_format = st.radio("Formato de Exportação", ["CSV", "JSON"])
            
            if export_format == "CSV":
                csv_data = card_manager.export_collection(format='csv')
                st.download_button(
                    label="Baixar como CSV",
                    data=csv_data,
                    file_name="mtg_collection.csv",
                    mime="text/csv"
                )
            else:
                json_data = card_manager.export_collection(format='json')
                st.download_button(
                    label="Baixar como JSON",
                    data=json_data,
                    file_name="mtg_collection.json",
                    mime="application/json"
                )
    
    with tab2:
        st.subheader("Importar Coleção")
        
        with st.form("import_form"):
            import_format = st.radio("Formato de Importação", ["CSV", "JSON"])
            import_mode = st.radio(
                "Modo de Importação", 
                ["Substituir coleção atual", "Mesclar com coleção atual"]
            )
            
            uploaded_file = st.file_uploader(
                f"Carregar arquivo {import_format}", 
                type=[import_format.lower()]
            )
            
            import_button = st.form_submit_button("Importar")
            
            if import_button and uploaded_file is not None:
                merge = import_mode == "Mesclar com coleção atual"
                success = card_manager.import_collection(
                    uploaded_file,
                    format=import_format.lower(),
                    merge=merge
                )
                
                if success:
                    st.success("Coleção importada com sucesso!")
                    st.rerun()
                else:
                    st.error("Erro ao importar coleção. Verifique o formato do arquivo.")