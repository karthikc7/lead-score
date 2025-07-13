from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# In-memory storage for leads
leads_storage = []

def validate_lead_data(data):
    """Validate lead data"""
    required_fields = ['phone_number', 'email', 'credit_score', 'age_group', 'family_background', 'income', 'comments', 'consent']
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing field: {field}"
    
    if not data['consent']:
        return False, "Consent must be given"
    
    try:
        credit_score = int(data['credit_score'])
        if credit_score < 300 or credit_score > 850:
            return False, "Credit score must be between 300 and 850"
    except (ValueError, TypeError):
        return False, "Credit score must be a valid number"
    
    try:
        income = int(data['income'])
        if income < 0:
            return False, "Income must be non-negative"
    except (ValueError, TypeError):
        return False, "Income must be a valid number"
    
    return True, None

def simple_score_calculation(data):
    """
    Simplified scoring algorithm without ML dependencies
    """
    base_score = 30  # Base score
    
    # Credit score factor (0-40 points)
    credit_score = int(data['credit_score'])
    credit_factor = ((credit_score - 300) / 550) * 40
    
    # Income factor (0-20 points)
    income = int(data['income'])
    income_factor = min((income / 1000000) * 20, 20)
    
    # Age group factor
    age_factors = {
        '18-25': 5,
        '26-35': 15,
        '36-50': 10,
        '51+': 5
    }
    age_factor = age_factors.get(data['age_group'], 5)
    
    # Family background factor
    family_factors = {
        'Single': 5,
        'Married': 10,
        'Married with Kids': 15
    }
    family_factor = family_factors.get(data['family_background'], 5)
    
    initial_score = base_score + credit_factor + income_factor + age_factor + family_factor
    return min(initial_score, 100)

def rerank_score(initial_score, comments):
    """
    Rule-based re-ranker to simulate LLM behavior.
    Adjusts the ML model's score based on keywords in comments.
    """
    score_adjustment = 0
    comments_lower = comments.lower()
    
    # Positive keywords
    positive_keywords = {
        'urgent': 15,
        'interested': 10,
        'ready': 12,
        'buy': 20,
        'purchase': 18,
        'need': 8,
        'want': 8,
        'asap': 15,
        'immediately': 12,
        'soon': 10,
        'hot': 15,
        'qualified': 12
    }
    
    # Negative keywords
    negative_keywords = {
        'not interested': -20,
        'maybe': -5,
        'later': -8,
        'thinking': -3,
        'unsure': -10,
        'budget': -5,
        'expensive': -12,
        'cheap': -8,
        'free': -10,
        'spam': -25,
        'unsubscribe': -30
    }
    
    # Check for positive keywords
    for keyword, adjustment in positive_keywords.items():
        if keyword in comments_lower:
            score_adjustment += adjustment
    
    # Check for negative keywords
    for keyword, adjustment in negative_keywords.items():
        if keyword in comments_lower:
            score_adjustment += adjustment
    
    # Apply adjustment and cap between 0-100
    reranked_score = initial_score + score_adjustment
    return max(0, min(100, reranked_score))

@app.route('/')
def serve_frontend():
    """Serve the React frontend"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    """Serve static files"""
    try:
        return send_from_directory(app.static_folder, path)
    except:
        # If file not found, serve index.html for SPA routing
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/score', methods=['POST'])
def score_lead():
    """Score a lead using simplified algorithm and apply LLM re-ranking."""
    try:
        data = request.get_json()
        
        # Validate input data
        is_valid, error_msg = validate_lead_data(data)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Calculate initial score using simplified algorithm
        initial_score = simple_score_calculation(data)
        
        # Apply LLM re-ranker
        reranked_score = rerank_score(initial_score, data['comments'])
        
        # Create lead score object
        lead_score = {
            'email': data['email'],
            'initial_score': round(initial_score, 2),
            'reranked_score': round(reranked_score, 2),
            'comments': data['comments']
        }
        
        # Store in memory
        leads_storage.append(lead_score)
        
        return jsonify(lead_score)
        
    except Exception as e:
        return jsonify({'error': f'Error processing lead: {str(e)}'}), 500

@app.route('/api/leads', methods=['GET'])
def get_leads():
    """Get all stored leads."""
    return jsonify({'leads': leads_storage})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'message': 'Lead Scoring API is running'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

