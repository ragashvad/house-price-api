"""
Model loading and prediction logic for the House Price API.
"""

import torch
from torch import nn
from pathlib import Path


# ============================================================
# 1. Define the model architecture (must match training!)
# ============================================================
class HousePriceModel(nn.Module):
    """Linear regression model for house price prediction."""
    
    def __init__(self):
        super().__init__()
        self.linear_layer = nn.Linear(in_features=3, out_features=1)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.linear_layer(x)


# ============================================================
# 2. Load the trained model & normalization parameters
# ============================================================
MODEL_DIR = Path(__file__).parent.parent / "models"
MODEL_PATH = MODEL_DIR / "house_price_model.pth"
NORM_PATH = MODEL_DIR / "normalization_params.pth"

# Create a fresh model instance
model = HousePriceModel()

# Load the trained weights into it
model.load_state_dict(torch.load(MODEL_PATH, weights_only=True))

# Set to evaluation mode (disables training-only behaviors)
model.eval()

# Load normalization parameters
norm_params = torch.load(NORM_PATH, weights_only=True)
X_min = norm_params['X_min']
X_max = norm_params['X_max']

print(f"✓ Model loaded from {MODEL_PATH}")
print(f"✓ Normalization params loaded: X_min={X_min}, X_max={X_max}")


# ============================================================
# 3. Prediction function
# ============================================================
def predict_price(size: float, bedrooms: int, age: float) -> float:
    """
    Predict house price given features.
    
    Args:
        size: House size in square meters
        bedrooms: Number of bedrooms
        age: Age of house in years
    
    Returns:
        Predicted price in thousands of dollars
    """
    # Convert inputs to a tensor of shape [1, 3]
    features = torch.tensor([[size, float(bedrooms), age]], dtype=torch.float32)
    
    # Apply the SAME normalization used during training
    features_norm = (features - X_min) / (X_max - X_min)
    
    # Make prediction (no gradient tracking needed)
    with torch.inference_mode():
        prediction = model(features_norm)
    
    # Extract the scalar value from the tensor
    return prediction.item()

# ============================================================
# 4. Standalone test (only runs when executed directly)
# ============================================================
if __name__ == "__main__":
    print("\n🧪 Testing prediction...")
    
    # Test case from your notebook: 180 m², 3 bedrooms, 12 years old
    price = predict_price(size=180, bedrooms=3, age=12)
    print(f"Predicted price: ${price:.2f}k")
    print(f"Expected: ~$534.90k")