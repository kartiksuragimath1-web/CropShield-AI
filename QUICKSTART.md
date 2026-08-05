# CropShield AI - Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Generate Sample Dataset
```bash
cd datasets
python generate_village_dataset.py
cd ..
```

### Step 3: Train Spread Prediction Model (Optional but Recommended)
```bash
cd ml_models
python train_spread_model.py
cd ..
```

### Step 4: Run the Application
```bash
cd backend
python app.py
```

### Step 5: Open Browser
Navigate to: **http://localhost:5000**

## 📋 What You'll See

1. **Home Page**: Project overview and features
2. **Upload Image**: Test disease detection
3. **Predict Spread**: Test spread risk prediction
4. **Risk Map**: View village risk visualization
5. **Admin Dashboard**: View analytics and statistics

## 🧪 Quick Test

### Test Disease Detection:
1. Go to `/upload`
2. Select a crop type
3. Upload any image (system uses fallback if model not trained)
4. View results

### Test Spread Prediction:
1. Go to `/predict-spread`
2. Fill in village details
3. Enter environmental data
4. Get risk prediction

## ⚠️ Important Notes

- **Disease Detection Model**: Works with fallback prediction even without training
- **Spread Prediction Model**: Should be trained for best results (see Step 3)
- **Database**: Automatically created on first run
- **Port**: Default is 5000, change in `backend/app.py` if needed

## 🐛 Troubleshooting

**Port already in use?**
- Change port: `app.run(port=5001)` in `backend/app.py`

**Import errors?**
- Ensure virtual environment is activated
- Run: `pip install -r requirements.txt`

**Models not found?**
- System uses fallback predictions automatically
- Train models using scripts in `ml_models/` folder

## 📚 Full Documentation

See `README.md` for complete documentation.
