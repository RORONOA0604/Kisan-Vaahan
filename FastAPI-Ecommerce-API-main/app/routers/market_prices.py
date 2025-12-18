from fastapi import APIRouter, status
from typing import Dict, Any

router = APIRouter(tags=["Market Prices"], prefix="/market-prices")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_market_prices(limit: int = 10) -> Dict[str, Any]:
    """
    Returns dummy market prices data.
    The external API (data.gov.in) is not accessible, so we return static data.
    """
    # Dummy market price data
    dummy_data = [
        {"commodity": "Tomato", "modal_price": "45", "market": "Delhi", "variety": "Local"},
        {"commodity": "Onion", "modal_price": "30", "market": "Mumbai", "variety": "Nashik"},
        {"commodity": "Potato", "modal_price": "25", "market": "Bangalore", "variety": "Local"},
        {"commodity": "Green Chilli", "modal_price": "60", "market": "Pune", "variety": "G4"},
        {"commodity": "Carrot", "modal_price": "35", "market": "Delhi", "variety": "Desi"},
        {"commodity": "Cabbage", "modal_price": "20", "market": "Chennai", "variety": "Green"},
        {"commodity": "Cauliflower", "modal_price": "40", "market": "Hyderabad", "variety": "White"},
        {"commodity": "Brinjal", "modal_price": "28", "market": "Kolkata", "variety": "Long"},
        {"commodity": "Beans", "modal_price": "50", "market": "Jaipur", "variety": "French"},
        {"commodity": "Peas", "modal_price": "55", "market": "Lucknow", "variety": "Green"}
    ]
    
    # Return limited results
    limited_data = dummy_data[:limit]
    
    return {
        "message": "Market prices fetched successfully (dummy data)",
        "data": limited_data
    }
