"""
Generate Synthetic Village Dataset
Creates a realistic dataset for training the spread prediction model.
"""

import pandas as pd
import numpy as np
import random

# Village names (Indian context)
VILLAGE_NAMES = [
    "Rampur", "Devgarh", "Khandwa", "Bilaspur", "Jhansi",
    "Ratlam", "Ujjain", "Indore", "Bhopal", "Gwalior",
    "Jabalpur", "Sagar", "Chhindwara", "Betul", "Hoshangabad",
    "Sehore", "Vidisha", "Raisen", "Damoh", "Chhatarpur",
    "Tikamgarh", "Panna", "Satna", "Rewa", "Sidhi",
    "Shahdol", "Anuppur", "Dindori", "Mandla", "Balaghat"
]

CROP_TYPES = ["Tomato", "Potato", "Corn", "Wheat", "Rice", "Cotton", "Soybean"]
DISEASES = [
    "Early Blight", "Late Blight", "Bacterial Spot", "Common Rust",
    "Leaf Spot", "Powdery Mildew", "Downy Mildew", "Anthracnose"
]

def generate_village_dataset(num_villages=200, output_path='village_dataset.csv'):
    """
    Generate synthetic village dataset with realistic features.
    
    Args:
        num_villages: Number of villages to generate
        output_path: Path to save CSV file
    """
    print(f"Generating dataset with {num_villages} villages...")
    
    data = []
    
    for i in range(num_villages):
        village_id = f"V{i+1:03d}"
        village_name = random.choice(VILLAGE_NAMES) + f" {i % 10 + 1}"
        
        # Generate coordinates (India region: 20-30°N, 70-85°E)
        latitude = round(random.uniform(20.0, 30.0), 4)
        longitude = round(random.uniform(70.0, 85.0), 4)
        
        crop_type = random.choice(CROP_TYPES)
        detected_disease = random.choice(DISEASES)
        
        # Generate weather data (realistic ranges)
        temperature = round(random.uniform(18.0, 35.0), 1)
        humidity = round(random.uniform(40.0, 90.0), 1)
        rainfall = round(random.uniform(0.0, 50.0), 1)
        wind_speed = round(random.uniform(2.0, 20.0), 1)
        
        # Generate outbreak history
        previous_outbreak_count = random.randint(0, 5)
        
        # Generate distance from infected village (km)
        distance_from_infected = round(random.uniform(0.5, 50.0), 1)
        
        # Calculate risk level based on features
        risk_score = 0
        
        # Temperature factor (20-30°C optimal for disease spread)
        if 20 <= temperature <= 30:
            risk_score += 2
        elif 15 <= temperature <= 35:
            risk_score += 1
        
        # Humidity factor (high humidity increases risk)
        if humidity > 70:
            risk_score += 2
        elif humidity > 60:
            risk_score += 1
        
        # Rainfall factor
        if rainfall > 20:
            risk_score += 2
        elif rainfall > 10:
            risk_score += 1
        
        # Wind speed factor (moderate wind spreads disease)
        if 5 <= wind_speed <= 15:
            risk_score += 2
        
        # Previous outbreak factor
        risk_score += min(previous_outbreak_count, 3)
        
        # Distance factor (closer = higher risk)
        if distance_from_infected < 5:
            risk_score += 3
        elif distance_from_infected < 10:
            risk_score += 2
        elif distance_from_infected < 20:
            risk_score += 1
        
        # Determine risk level
        if risk_score >= 8:
            risk_level = "High"
        elif risk_score >= 5:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        data.append({
            'village_id': village_id,
            'village_name': village_name,
            'latitude': latitude,
            'longitude': longitude,
            'crop_type': crop_type,
            'detected_disease': detected_disease,
            'temperature': temperature,
            'humidity': humidity,
            'rainfall': rainfall,
            'wind_speed': wind_speed,
            'previous_outbreak_count': previous_outbreak_count,
            'distance_from_infected_village': distance_from_infected,
            'spread_risk_level': risk_level
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"Dataset saved to: {output_path}")
    print(f"\nDataset Statistics:")
    print(f"Total villages: {len(df)}")
    print(f"\nRisk Level Distribution:")
    print(df['spread_risk_level'].value_counts())
    print(f"\nCrop Type Distribution:")
    print(df['crop_type'].value_counts())
    print(f"\nDisease Distribution:")
    print(df['detected_disease'].value_counts())
    
    return df

if __name__ == '__main__':
    import sys
    
    num_villages = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    output_path = sys.argv[2] if len(sys.argv) > 2 else 'village_dataset.csv'
    
    generate_village_dataset(num_villages, output_path)
