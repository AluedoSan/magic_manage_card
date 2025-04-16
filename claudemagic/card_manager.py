import pandas as pd
import os
from datetime import datetime

class CardManager:
    def __init__(self):
        self.file_path = "mtg_collection.csv"
        self.load_collection()
    
    def load_collection(self):
        """Carrega a coleção do arquivo CSV ou cria um DataFrame vazio se não existir"""
        if os.path.exists(self.file_path):
            self.collection = pd.read_csv(self.file_path)
        else:
            self.collection = pd.DataFrame({
                'name': [],
                'edition': [],
                'card_type': [],
                'rarity': [],
                'colors': [],
                'cmc': [],
                'quantity': [],
                'condition': [],
                'price_bought': [],
                'price_current': [],
                'foil': [],
                'date_added': []
            })
    
    def save_collection(self):
        """Salva a coleção em um arquivo CSV"""
        self.collection.to_csv(self.file_path, index=False)
    
    def add_card(self, card_data):
        """Adiciona uma nova carta à coleção"""
        # Adiciona a data atual
        card_data['date_added'] = datetime.now().strftime("%Y-%m-%d")
        
        # Converte cores em string separada por vírgulas se for uma lista
        if isinstance(card_data['colors'], list):
            card_data['colors'] = ','.join(card_data['colors'])
            
        # Verifica se a carta já existe na coleção
        mask = (
            (self.collection['name'] == card_data['name']) & 
            (self.collection['edition'] == card_data['edition']) &
            (self.collection['foil'] == card_data['foil']) &
            (self.collection['condition'] == card_data['condition'])
        )
        
        if mask.any():
            # Atualiza a quantidade se a carta já existir
            idx = self.collection[mask].index[0]
            self.collection.at[idx, 'quantity'] += card_data['quantity']
            # Atualiza o preço atual
            self.collection.at[idx, 'price_current'] = card_data['price_current']
        else:
            # Adiciona uma nova linha para uma nova carta
            self.collection = pd.concat([
                self.collection, 
                pd.DataFrame([card_data])
            ], ignore_index=True)
        
        self.save_collection()
        return True
    
    def update_card(self, index, card_data):
        """Atualiza as informações de uma carta existente"""
        for key, value in card_data.items():
            self.collection.at[index, key] = value
        self.save_collection()
        return True
    
    def remove_card(self, index, quantity=None):
        """Remove uma carta ou reduz sua quantidade"""
        if quantity is None or quantity >= self.collection.at[index, 'quantity']:
            self.collection = self.collection.drop(index)
        else:
            self.collection.at[index, 'quantity'] -= quantity
        
        self.save_collection()
        return True
    
    def search_cards(self, query, field):
        """Busca cartas pelo critério especificado"""
        if field == 'all':
            # Busca em todos os campos
            result = pd.DataFrame()
            for column in self.collection.columns:
                if self.collection[column].dtype == 'object':  # apenas campos de texto
                    matches = self.collection[self.collection[column].astype(str).str.contains(query, case=False, na=False)]
                    result = pd.concat([result, matches])
            return result.drop_duplicates()
        else:
            # Busca em um campo específico
            return self.collection[self.collection[field].astype(str).str.contains(query, case=False, na=False)]
    
    def get_stats(self):
        """Retorna estatísticas da coleção"""
        stats = {
            'total_cards': self.collection['quantity'].sum(),
            'unique_cards': len(self.collection),
            'total_value': (self.collection['price_current'] * self.collection['quantity']).sum(),
            'cards_by_color': self.get_cards_by_color(),
            'cards_by_rarity': self.collection.groupby('rarity')['quantity'].sum().to_dict(),
            'cards_by_type': self.collection.groupby('card_type')['quantity'].sum().to_dict(),
            'cards_by_edition': self.collection.groupby('edition')['quantity'].sum().to_dict()
        }
        return stats
    
    def get_cards_by_color(self):
        """Retorna a contagem de cartas por cor"""
        # Lidar com múltiplas cores em uma única carta
        color_counts = {}
        for _, row in self.collection.iterrows():
            colors = str(row['colors']).split(',')
            for color in colors:
                color = color.strip()
                if color:
                    if color not in color_counts:
                        color_counts[color] = 0
                    color_counts[color] += row['quantity']
        return color_counts
    
    def export_collection(self, format='csv'):
        """Exporta a coleção para o formato especificado"""
        if format == 'csv':
            return self.collection.to_csv(index=False)
        elif format == 'json':
            return self.collection.to_json(orient='records')
        else:
            raise ValueError(f"Formato não suportado: {format}")
    
    def import_collection(self, data, format='csv', merge=False):
        """Importa uma coleção do formato especificado"""
        try:
            if format == 'csv':
                imported_collection = pd.read_csv(data)
            elif format == 'json':
                imported_collection = pd.read_json(data)
            else:
                raise ValueError(f"Formato não suportado: {format}")
            
            if merge:
                # Mescla as coleções
                self.collection = pd.concat([self.collection, imported_collection]).drop_duplicates(
                    subset=['name', 'edition', 'foil', 'condition'], keep='first'
                )
            else:
                # Substitui a coleção atual
                self.collection = imported_collection
            
            self.save_collection()
            return True
        except Exception as e:
            print(f"Erro ao importar coleção: {e}")
            return False