import random

def get_card_image_url(card_name, edition):
    """
    Retorna uma URL de imagem para a carta especificada.
    Essa função é apenas um exemplo e não faz uma chamada real à API.
    Na implementação real, você poderia usar a API do Scryfall ou similar.
    """
    # Na versão real, isso faria uma chamada à API do Scryfall ou similar
    # Como é apenas um exemplo, retornamos um placeholder
    return "https://via.placeholder.com/265x370/0000FF/FFFFFF?text=" + card_name.replace(" ", "+")

def validate_card(card_data):
    """
    Valida os dados de uma carta antes de adicioná-la à coleção.
    """
    # Verifica se os campos obrigatórios estão presentes
    required_fields = ['name', 'edition']
    
    for field in required_fields:
        if not card_data.get(field):
            return {
                'valid': False,
                'error': f"Campo obrigatório ausente: {field}"
            }
    
    # Validação de tipo de dados
    if not isinstance(card_data.get('quantity', 1), (int, float)) or card_data.get('quantity', 1) <= 0:
        return {
            'valid': False,
            'error': "Quantidade deve ser um número positivo"
        }
    
    if not isinstance(card_data.get('price_bought', 0), (int, float)) or card_data.get('price_bought', 0) < 0:
        return {
            'valid': False,
            'error': "Preço de compra deve ser um número não negativo"
        }
    
    if not isinstance(card_data.get('price_current', 0), (int, float)) or card_data.get('price_current', 0) < 0:
        return {
            'valid': False,
            'error': "Preço atual deve ser um número não negativo"
        }
    
    return {
        'valid': True
    }

def search_card_by_name(card_name):
    """
    Busca informações de uma carta por nome.
    Essa função é apenas um exemplo e não faz uma chamada real à API.
    Na implementação real, você poderia usar a API do Scryfall ou similar.
    """
    # Simula uma resposta de uma API de MTG
    # Em uma implementação real, você faria uma chamada a uma API como:
    # response = requests.get(f"https://api.scryfall.com/cards/named?fuzzy={card_name}")
    
    dummy_data = {
        'name': card_name,
        'edition': random.choice(['Dominaria', 'Core Set 2021', 'Kamigawa', 'Ikoria']),
        'card_type': random.choice(['Criatura', 'Mágica Instantânea', 'Feitiço', 'Encantamento']),
        'rarity': random.choice(['Comum', 'Incomum', 'Rara', 'Mítica']),
        'colors': random.choice([['Branco'], ['Azul'], ['Preto'], ['Vermelho'], ['Verde'], ['Branco', 'Azul']]),
        'cmc': random.randint(1, 7),
        'price_current': round(random.uniform(0.5, 50.0), 2)
    }
    
    return {
        'success': True,
        'data': dummy_data
    }

def generate_mock_collection(num_cards=20):
    """
    Gera uma coleção de cartas aleatória para fins de demonstração.
    """
    card_names = [
        "Dragão Ancião", "Gigante de Pedra", "Anjo Protetor", "Necromante Sombrio",
        "Elfo Arqueiro", "Troll Regenerador", "Lobisomem Alfa", "Contramágica",
        "Caminhante Mental", "Chamas Devastadoras", "Crescimento Selvagem",
        "Lich Imortal", "Hidra Voraz", "Behemoth Colossal", "Espectro Noturno",
        "Fênix Renascida", "Golem de Cristal", "Druida da Floresta", "Vampiro Nobre",
        "Mago do Tempo", "Guerreiro Destemido", "Sacerdote da Luz", "Goblin Astuto"
    ]
    
    editions = ["Dominaria", "Ravnica", "Kamigawa", "Innistrad", "Zendikar", "Theros", "Eldraine"]
    rarities = ["Comum", "Incomum", "Rara", "Mítica"]
    types = ["Criatura", "Mágica Instantânea", "Feitiço", "Encantamento", "Artefato", "Planeswalker", "Terra"]
    conditions = ["Mint", "Near Mint", "Excellent", "Good", "Light Played", "Played"]
    
    mock_collection = []
    
    for _ in range(min(num_cards, len(card_names))):
        card_name = card_names.pop()
        
        # Gera cores aleatórias
        num_colors = random.randint(1, 3)
        all_colors = ["Branco", "Azul", "Preto", "Vermelho", "Verde"]
        colors = random.sample(all_colors, num_colors)
        
        mock_card = {
            'name': card_name,
            'edition': random.choice(editions),
            'card_type': random.choice(types),
            'rarity': random.choice(rarities),
            'colors': ','.join(colors),
            'cmc': random.randint(1, 8),
            'quantity': random.randint(1, 4),
            'condition': random.choice(conditions),
            'price_bought': round(random.uniform(0.5, 30.0), 2),
            'price_current': round(random.uniform(0.5, 50.0), 2),
            'foil': random.random() > 0.8,
            'date_added': f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
        }
        
        mock_collection.append(mock_card)
    
    return mock_collection