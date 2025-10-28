from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS so frontend can call backend

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Example: extract all paragraph texts
        paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]

        return jsonify({'paragraphs': paragraphs})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

import os

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
