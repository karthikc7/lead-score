from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, field_validator
import joblib
import pandas as pd
import re
from typing import Optional

# Load the trained model
model = joblib.load('lead_scoring_model.pkl')

# Initialize FastAPI app
app = FastAPI(title="Lead Scoring API", description="API for scoring leads using ML and LLM re-ranker")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# In-memory storage for leads
leads_storage = []

# Pydantic models for request/response
class LeadData(BaseModel):
    phone_number: str
    email: EmailStr
    credit_score: int
    age_group: str
    family_background: str
    income: int
    comments: str
    consent: bool
    
    @field_validator('credit_score')
    @classmethod
    def validate_credit_score(cls, v):
        if v < 300 or v > 850:
            raise ValueError('Credit score must be between 300 and 850')
        return v
    
    @field_validator('income')
    @classmethod
    def validate_income(cls, v):
        if v < 0:
            raise ValueError('Income must be non-negative')
        return v
    
    @field_validator('consent')
    @classmethod
    def validate_consent(cls, v):
        if not v:
            raise ValueError('Consent must be given')
        return v

class LeadScore(BaseModel):
    email: str
    initial_score: float
    reranked_score: float
    comments: str

# LLM-inspired re-ranker
def rerank_score(initial_score: float, comments: str) -> float:
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

def encode_categorical_features(lead_data: LeadData):
    """
    Encode categorical features to match the training data encoding.
    This is a simplified version - in production, you'd save the encoders.
    """
    # Mapping for Lead Origin (simplified)
    lead_origin_map = {
        'api': 0,
        'landing page submission': 1,
        'quick add form': 2,
        'reference': 3
    }
    
    # Mapping for Lead Source (simplified)
    lead_source_map = {
        'direct traffic': 0,
        'google': 1,
        'organic search': 2,
        'olark chat': 3,
        'reference': 4,
        'welingak website': 5,
        'facebook': 6,
        'bing': 7,
        'social media': 8,
        'youtubechannel': 9
    }
    
    # For this demo, we'll use default values
    # In a real implementation, you'd extract these from the form
    lead_origin = 1  # Default to 'landing page submission'
    lead_source = 1  # Default to 'google'
    
    return lead_origin, lead_source

@app.post("/score", response_model=LeadScore)
async def score_lead(lead_data: LeadData):
    """
    Score a lead using the ML model and apply LLM re-ranking.
    """
    try:
        # Encode categorical features
        lead_origin, lead_source = encode_categorical_features(lead_data)
        
        # Create feature vector for prediction
        # Features: TotalVisits, Total Time Spent on Website, Page Views Per Visit, Lead Origin, Lead Source
        # For new leads, we'll use default values for web activity
        features = pd.DataFrame({
            'TotalVisits': [1],  # Default for new lead
            'Total Time Spent on Website': [300],  # Default 5 minutes
            'Page Views Per Visit': [2],  # Default
            'Lead Origin': [lead_origin],
            'Lead Source': [lead_source]
        })
        
        # Get prediction probability (0-1)
        prediction_proba = model.predict_proba(features)[0][1]  # Probability of conversion
        
        # Scale to 0-100
        initial_score = prediction_proba * 100
        
        # Apply LLM re-ranker
        reranked_score = rerank_score(initial_score, lead_data.comments)
        
        # Create lead score object
        lead_score = LeadScore(
            email=lead_data.email,
            initial_score=round(initial_score, 2),
            reranked_score=round(reranked_score, 2),
            comments=lead_data.comments
        )
        
        # Store in memory
        leads_storage.append(lead_score.model_dump())
        
        return lead_score
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing lead: {str(e)}")

@app.get("/leads")
async def get_leads():
    """
    Get all stored leads.
    """
    return {"leads": leads_storage}

@app.get("/")
async def root():
    return {"message": "Lead Scoring API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

