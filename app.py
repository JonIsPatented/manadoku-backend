from flask import Flask, jsonify, request
from flask_cors import CORS

import asyncio
import scrython

app = Flask(__name__)
# Set a secret key for session management (important for games)
app.secret_key = 'your_super_secret_key' 

CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

@app.route('/api/guess', methods=['POST'])
def guess():
    data = request.get_json()

    card_name = data["cardName"]
    row_filter = data["rowFilter"]
    col_filter = data["colFilter"]

    is_valid = False
    image_url = None

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        cards = scrython.cards.Search(q=(
            f"game:paper not:extras {row_filter} "
            f"{col_filter} "
        ), cache=True)

        found_card = next((card for card in cards.iter_all() if card.name == card_name),
                          None)

        if found_card is not None:
            image_url = found_card.get_image_url()

        loop.close()

        if image_url is not None:
            is_valid = True

    except Exception as e:
        print(f"Error: {e}")

    return jsonify({
        "valid": is_valid,
        "card": {
            "name": card_name,
            "imageUrl": image_url
        }
    })

@app.route('/api/stats', methods=['GET'])
def stats():
    return jsonify({
        "high_score": 100,
        "rounds_played": 20
    })

@app.route('/api/card-names/<string:prefix>', methods=['GET'])
@app.route('/api/card-names/', defaults={'prefix': ""}, methods=['GET'])
def card_names(prefix: str):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        cards = scrython.cards.Search(q=f"game:paper not:extra name:/^{prefix}/", cache=True)
        cardNames = sorted([card.name for card in cards.iter_all(cache=True)])

        loop.close()

        return cardNames

    except Exception as e:
        print(f"Error: {e}")
        return sorted([
            "Llanowar Elves",
            "Black Lotus",
            "Lotus Cobra",
            "Lightning Bolt",
            "Counterspell",
        ])

@app.route('/api/categories/<int:game_seed>', methods=['GET'])
def getCategories(game_seed: int):
    return [
        {
            "summary": "Mana Value 5",
            "description": "This card has a mana value of 5.",
            "filter": "mv=5"
        },
        {
            "summary": "Phyrexian Mana",
            "description": "This card contains phyrexian mana symbols in its mana cost or rules text.",
            "filter": "is:phyrexian"
        },
        {
            "summary": "Merfolk",
            "description": "This card is has the Merfolk creature type.",
            "filter": "t:merfolk"
        },
        {
            "summary": "Sorcery",
            "description": "This card is has the sorcery type.",
            "filter": "t:sorcery"
        },
        {
            "summary": "Deathtouch",
            "description": "This card has deathtouch.",
            "filter": "kw:deathtouch"
        },
        {
            "summary": "Hybrid Mana",
            "description": "This card contains hybrid mana symbols in its mana cost or rules text.",
            "filter": "is:hybrid"
        }
    ]

if __name__ == '__main__':
    # Run the app in debug mode for development
    app.run(debug=True)

