# CropShield AI – Predicting Crop Disease Spread Across Villages

A comprehensive AI-powered system for detecting crop diseases from leaf images and predicting disease spread risk across villages. Built as a Computer Science 6th Semester main project.

## 🎯 Project Overview

CropShield AI combines deep learning for disease detection with machine learning for spread prediction, providing farmers and agriculture officers with early warnings and actionable insights.

### Key Features

1. **Disease Detection**: Upload leaf images to detect crop diseases using CNN models
2. **Spread Prediction**: Predict disease spread risk across nearby villages using ML algorithms
3. **Risk Visualization**: Interactive map dashboard showing village-wise risk levels
4. **Analytics Dashboard**: Comprehensive statistics and insights for administrators

## 🏗️ Project Structure

```
cropshield-ai/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── models/                # Saved ML models
│   ├── routes/                # API route handlers
│   │   ├── disease_routes.py
│   │   ├── spread_routes.py
│   │   └── dashboard_routes.py
│   ├── services/              # Business logic services
│   │   ├── database_service.py
│   │   ├── disease_service.py
│   │   └── spread_service.py
│   ├── uploads/               # Uploaded images storage
│   └── templates/             # Flask templates (symlinked)
│
├── frontend/
│   ├── templates/             # HTML templates
│   │   ├── index.html
│   │   ├── upload.html
│   │   ├── predict_spread.html
│   │   ├── map_dashboard.html
│   │   └── admin_dashboard.html
│   └── static/
│       └── css/
│           └── style.css
│
├── ml_models/
│   ├── train_disease_model.py    # CNN training script
│   └── train_spread_model.py      # Random Forest training script
│
├── datasets/
│   ├── generate_village_dataset.py
│   └── village_dataset.csv        # Generated dataset
│
├── requirements.txt
└── README.md
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional)

### Installation Steps

1. **Clone or download the project**
   ```bash
   cd cropshield-ai
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate sample dataset**
   ```bash
   cd datasets
   python generate_village_dataset.py
   cd ..
   ```

5. **Train ML models (optional - models will use fallback if not trained)**
   ```bash
   # Train disease detection model (requires PlantVillage dataset or uses synthetic data)
   cd ml_models
   python train_disease_model.py
   
   # Train spread prediction model
   python train_spread_model.py
   cd ..
   ```

6. **Run the application**
   ```bash
   cd backend
   python app.py
   ```

7. **Access the application**
   - Open your browser and navigate to: `http://localhost:5000`
   - The application will be running on port 5000

## 📊 Dataset Information

### 1. PlantVillage Dataset (for Disease Detection)

The project uses the PlantVillage dataset structure for training the disease detection CNN model. The dataset includes:

- **25 disease classes** across 5 crop types:
  - Apple (4 classes)
  - Corn (4 classes)
  - Grape (4 classes)
  - Potato (3 classes)
  - Tomato (10 classes)

**Note**: For demo purposes, the system includes fallback prediction logic. For production, download the PlantVillage dataset from:
- [PlantVillage Dataset](https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset)

### 2. Village Dataset (for Spread Prediction)

The synthetic village dataset includes the following features:

- **Village Information**: ID, name, coordinates
- **Crop Information**: Crop type, detected disease
- **Environmental Factors**: Temperature, humidity, rainfall, wind speed
- **Historical Data**: Previous outbreak count, distance from infected village
- **Target Variable**: Spread risk level (Low, Medium, High)

**Dataset Generation**:
```bash
python datasets/generate_village_dataset.py [num_villages] [output_file]
```

## 🤖 Machine Learning Models

### 1. Disease Detection Model (CNN)

**Architecture**:
- Input: 224x224 RGB images
- Convolutional layers with max pooling
- Dropout for regularization
- Dense layers for classification
- Output: 25 disease classes

**Training**:
```bash
python ml_models/train_disease_model.py [path_to_plantvillage_dataset]
```

**Usage**: The model analyzes uploaded leaf images and returns:
- Detected disease name
- Confidence score (0-100%)
- Crop type

### 2. Spread Prediction Model (Random Forest)

**Features**:
- Temperature (°C)
- Humidity (%)
- Rainfall (mm)
- Wind Speed (km/h)
- Previous Outbreak Count
- Distance from Infected Village (km)

**Training**:
```bash
python ml_models/train_spread_model.py [path_to_village_dataset.csv]
```

**Output**: Risk level (Low/Medium/High) and probability score

## 🌐 API Endpoints

### Disease Detection
- `POST /api/predict-disease`
  - Upload image file
  - Returns: disease name, confidence, crop type

### Spread Prediction
- `POST /api/predict-spread`
  - Send village data JSON
  - Returns: risk level and probability

### Dashboard
- `GET /api/risk-map`
  - Returns: All villages with risk levels and coordinates

- `GET /api/dashboard-stats`
  - Returns: Statistics for admin dashboard

- `GET /api/recent-predictions`
  - Returns: Recent disease predictions

## 🗄️ Database

The project uses SQLite database (`cropshield.db`) with three main tables:

1. **disease_predictions**: Stores disease detection results
2. **spread_predictions**: Stores spread risk predictions
3. **villages**: Stores village information and risk levels

The database is automatically initialized when the application starts.

## 🎨 Frontend Pages

1. **Home Page** (`/`): Project overview and features
2. **Upload Image** (`/upload`): Disease detection interface
3. **Predict Spread** (`/predict-spread`): Spread risk prediction form
4. **Risk Map** (`/map-dashboard`): Interactive map with village markers
5. **Admin Dashboard** (`/admin-dashboard`): Analytics and statistics

## 🔧 Configuration

### Environment Variables (Optional)

Create a `.env` file in the backend directory:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
```

## 📝 Usage Examples

### 1. Detect Disease from Image

1. Navigate to `/upload`
2. Select crop type
3. Upload leaf image
4. View detection results

### 2. Predict Spread Risk

1. Navigate to `/predict-spread`
2. Fill in village details
3. Enter environmental conditions
4. Submit to get risk prediction

### 3. View Risk Map

1. Navigate to `/map-dashboard`
2. View all villages on interactive map
3. Click markers for details
4. Review risk summary table

## 🧪 Testing

### Test Disease Detection API
```bash
curl -X POST http://localhost:5000/api/predict-disease \
  -F "image=@path/to/image.jpg" \
  -F "crop_type=Tomato"
```

### Test Spread Prediction API
```bash
curl -X POST http://localhost:5000/api/predict-spread \
  -H "Content-Type: application/json" \
  -d '{
    "village_id": "V001",
    "village_name": "Test Village",
    "crop_type": "Tomato",
    "detected_disease": "Early Blight",
    "temperature": 25.5,
    "humidity": 70.0,
    "rainfall": 15.0,
    "wind_speed": 10.0,
    "previous_outbreak_count": 2,
    "distance_from_infected_village": 5.0
  }'
```

## 🎓 Project Explanation (For Viva)

### Architecture
- **Backend**: Flask REST API with modular structure
- **Frontend**: HTML/CSS/JavaScript with Bootstrap
- **ML Models**: TensorFlow/Keras for CNN, Scikit-learn for Random Forest
- **Database**: SQLite for data persistence

### Key Algorithms
1. **CNN for Image Classification**: Convolutional neural network with multiple layers
2. **Random Forest for Risk Prediction**: Ensemble learning with feature importance
3. **Rule-based Fallback**: Ensures system works even without trained models

### Data Flow
1. User uploads image → Preprocessing → CNN prediction → Database storage
2. User submits village data → Feature extraction → Random Forest prediction → Risk assessment
3. Dashboard queries database → Aggregates statistics → Visualizes on map/charts

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   - Change port in `app.py`: `app.run(port=5001)`

2. **Model not found**
   - System uses fallback prediction automatically
   - Train models using training scripts

3. **Database errors**
   - Delete `cropshield.db` and restart application
   - Database will be recreated automatically

4. **Import errors**
   - Ensure virtual environment is activated
   - Reinstall requirements: `pip install -r requirements.txt`

## 📚 Technologies Used

- **Backend**: Python, Flask, SQLite
- **Machine Learning**: TensorFlow, Keras, Scikit-learn, NumPy, Pandas
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Visualization**: Leaflet.js (maps), Chart.js (charts)
- **Image Processing**: Pillow (PIL)

## 👥 Contributors

Computer Science 6th Semester Project

## 📄 License

This project is created for educational purposes.

## 🙏 Acknowledgments

- PlantVillage dataset for disease classification
- OpenStreetMap for map tiles
- Bootstrap and other open-source libraries

---

**Note**: This is a demonstration project. For production use, ensure proper model training, data validation, and security measures.
