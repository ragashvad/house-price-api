"""
FastAPI application for the House Price Prediction API.
"""

from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.model import predict_price


# ============================================================
# 1. Create the FastAPI app
# ============================================================
app = FastAPI(
    title="House Price Predictor",
    description="Predicts house prices based on size, bedrooms, and age.",
    version="1.0.0",
)

# Path to static files
STATIC_DIR = Path(__file__).parent.parent / "static"


# ============================================================
# 2. Pydantic schemas
# ============================================================
class HouseInput(BaseModel):
    size: float = Field(..., gt=0, description="Size in square meters")
    bedrooms: int = Field(..., ge=1, le=10, description="Number of bedrooms")
    age: float = Field(..., ge=0, description="Age of house in years")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"size": 180.0, "bedrooms": 3, "age": 12.0}
            ]
        }
    }


class PredictionOutput(BaseModel):
    predicted_price_thousands: float = Field(..., description="Predicted price in thousands of dollars")
    predicted_price_formatted: str = Field(..., description="Predicted price as a formatted string")


# ============================================================
# 3. Endpoints
# ============================================================
@app.get("/")
def root():
    """Serve the HTML frontend."""
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api")
def api_info():
    """API information endpoint."""
    return {
        "message": "House Price Predictor API is running!",
        "frontend": "/",
        "docs": "/docs",
        "predict": "POST /predict with size, bedrooms, age",
    }


@app.post("/predict", response_model=PredictionOutput)
def predict(house: HouseInput):
    """Predict the price of a house."""
    price = predict_price(
        size=house.size,
        bedrooms=house.bedrooms,
        age=house.age,
    )
    return PredictionOutput(
        predicted_price_thousands=round(price, 2),
        predicted_price_formatted=f"${price:.2f}k",
    )