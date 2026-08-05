"""
Setup script for CropShield AI
Initializes the project structure and generates sample data.
"""

import os
import subprocess
import sys

def create_directories():
    """Create necessary directories."""
    directories = [
        'backend/models',
        'backend/uploads',
        'backend/static',
        'backend/templates',
        'frontend/static/css',
        'frontend/static/images',
        'datasets'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def generate_dataset():
    """Generate sample village dataset."""
    print("\nGenerating sample village dataset...")
    try:
        subprocess.run([
            sys.executable,
            'datasets/generate_village_dataset.py',
            '200',
            'datasets/village_dataset.csv'
        ], check=True)
        print("✓ Dataset generated successfully")
    except Exception as e:
        print(f"⚠ Warning: Could not generate dataset: {e}")

def install_dependencies():
    """Install Python dependencies."""
    print("\nInstalling dependencies...")
    try:
        subprocess.run([
            sys.executable,
            '-m',
            'pip',
            'install',
            '-r',
            'requirements.txt'
        ], check=True)
        print("✓ Dependencies installed successfully")
    except Exception as e:
        print(f"⚠ Warning: Could not install dependencies: {e}")
        print("Please run: pip install -r requirements.txt")

def main():
    print("=" * 60)
    print("CropShield AI - Setup Script")
    print("=" * 60)
    
    print("\n1. Creating directory structure...")
    create_directories()
    
    print("\n2. Generating sample dataset...")
    generate_dataset()
    
    print("\n3. Installing dependencies...")
    install_dependencies()
    
    print("\n" + "=" * 60)
    print("Setup completed!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Train models (optional):")
    print("   cd ml_models")
    print("   python train_spread_model.py")
    print("\n2. Run the application:")
    print("   cd backend")
    print("   python app.py")
    print("\n3. Open browser:")
    print("   http://localhost:5000")
    print("=" * 60)

if __name__ == '__main__':
    main()
