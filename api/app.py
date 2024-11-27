import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

class AnimeQuotesAPI:
    def __init__(self, csv_path):
        """
        Initialize the API with the quotes dataset
        
        :param csv_path: Path to the CSV file containing quotes
        """
        try:
            self.quotes_df = pd.read_csv(csv_path)
        except Exception as e:
            raise ValueError(f"Error loading CSV: {e}")
    
    def get_random_quote(self):
        """
        Select a random quote from the dataset
        
        :return: Dictionary with quote details
        """
        random_quote = self.quotes_df.sample(n=1).iloc[0]
        return {
            "quote": random_quote['Quote'],
            "character": random_quote['Character'],
            "anime": random_quote['Anime']
        }
    
    def get_quotes_by_anime(self, anime_name):
        """
        Get quotes from a specific anime
        
        :param anime_name: Name of the anime
        :return: List of quotes from the specified anime
        """
        anime_quotes = self.quotes_df[self.quotes_df['Anime'].str.contains(anime_name, case=False)]
        return [
            {
                "quote": row['Quote'],
                "character": row['Character']
            } for _, row in anime_quotes.iterrows()
        ]
    
    def get_quotes_by_character(self, character_name):
        """
        Get quotes by a specific character
        
        :param character_name: Name of the character
        :return: List of quotes by the specified character
        """
        character_quotes = self.quotes_df[self.quotes_df['Character'].str.contains(character_name, case=False)]
        return [
            {
                "quote": row['Quote'],
                "anime": row['Anime']
            } for _, row in character_quotes.iterrows()
        ]
    
    def get_unique_animes(self):
        """
        Get list of unique animes in the dataset
        
        :return: List of unique anime names
        """
        return list(self.quotes_df['Anime'].unique())
    
    def get_quote_count(self):
        """
        Get total number of quotes
        
        :return: Total quote count
        """
        return len(self.quotes_df)

def create_app(csv_path='AnimeQuotes.csv'):
    """
    Create and configure Flask application
    
    :param csv_path: Path to the CSV file
    :return: Configured Flask app
    """
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    quotes_api = AnimeQuotesAPI(csv_path)
    
    @app.route('/random-quote', methods=['GET'])
    def random_quote():
        """
        Endpoint to get a random quote
        """
        try:
            quote = quotes_api.get_random_quote()
            return jsonify(quote), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/quotes/anime', methods=['GET'])
    def quotes_by_anime():
        """
        Endpoint to get quotes by anime name
        Query param: anime (case-insensitive)
        """
        anime = request.args.get('anime')
        if not anime:
            return jsonify({"error": "Anime name is required"}), 400
        
        quotes = quotes_api.get_quotes_by_anime(anime)
        return jsonify({
            "anime": anime,
            "quotes": quotes,
            "quote_count": len(quotes)
        }), 200
    
    @app.route('/quotes/character', methods=['GET'])
    def quotes_by_character():
        """
        Endpoint to get quotes by character name
        Query param: character (case-insensitive)
        """
        character = request.args.get('character')
        if not character:
            return jsonify({"error": "Character name is required"}), 400
        
        quotes = quotes_api.get_quotes_by_character(character)
        return jsonify({
            "character": character,
            "quotes": quotes,
            "quote_count": len(quotes)
        }), 200
    
    @app.route('/animes', methods=['GET'])
    def list_animes():
        """
        Endpoint to list all unique animes
        """
        animes = quotes_api.get_unique_animes()
        return jsonify({
            "animes": animes,
            "total_anime_count": len(animes)
        }), 200
    
    @app.route('/stats', methods=['GET'])
    def get_stats():
        """
        Endpoint to get overall stats
        """
        total_quotes = quotes_api.get_quote_count()
        unique_animes = quotes_api.get_unique_animes()
        
        return jsonify({
            "total_quotes": total_quotes,
            "total_unique_animes": len(unique_animes)
        }), 200
    
    return app

# Usage example
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)