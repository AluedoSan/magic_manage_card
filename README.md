# Magic Card Manager

Um aplicativo para gerenciar sua coleção de cartas de Magic: The Gathering, construído com Python e Streamlit.

## Funcionalidades

- **Adicionar Cartas**: Cadastre suas cartas com informações detalhadas
- **Visualizar Coleção**: Veja todas as suas cartas com filtros por edição, raridade e tipo
- **Buscar Cartas**: Encontre cartas específicas em sua coleção
- **Estatísticas**: Veja análises e gráficos da sua coleção
- **Exportar/Importar**: Faça backup dos seus dados ou migre de outros sistemas

## Requisitos

- Python 3.7+
- Streamlit
- Pandas
- Matplotlib
- Pillow
- Requests

## Instalação

1. Clone este repositório ou descompacte o arquivo ZIP baixado
2. Instale as dependências:

```bash
pip install -r requirements.txt
```
Ou para usuários de poetry:

```bash
poetry install
```

## Como executar

```bash
streamlit run app.py
```

O aplicativo será aberto automaticamente no seu navegador padrão.

## Estrutura do Projeto

- `app.py`: Ponto de entrada do aplicativo
- `card_manager.py`: Classe responsável pelo gerenciamento de cartas
- `ui_components.py`: Componentes da interface do usuário
- `card_utils.py`: Funções utilitárias

## Armazenamento de Dados

Seus dados são armazenados localmente em um arquivo CSV chamado `mtg_collection.csv`.

## Recursos Futuros

- Integração com APIs de cartas de Magic (como Scryfall)
- Detecção automática de preços atuais
- Imagens de cartas
- Gerenciamento de decks
- Estatísticas avançadas
- Histórico de preços

## Como Contribuir

1. Faça um fork do repositório
2. Crie uma branch para sua funcionalidade (`git checkout -b feature/nova-funcionalidade`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. Faça push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request
