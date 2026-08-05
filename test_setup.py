"""
Quick test script to verify CropShield AI setup
"""

import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists."""
    if os.path.exists(filepath):
        print(f"[OK] {description}: {filepath}")
        return True
    else:
        print(f"[FAIL] {description} NOT FOUND: {filepath}")
        return False

def check_directory_exists(dirpath, description):
    """Check if a directory exists."""
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        print(f"[OK] {description}: {dirpath}")
        return True
    else:
        print(f"[FAIL] {description} NOT FOUND: {dirpath}")
        return False

def main():
    print("=" * 60)
    print("CropShield AI - Setup Verification")
    print("=" * 60)
    
    checks_passed = 0
    checks_total = 0
    
    # Check backend files
    print("\nBackend Files:")
    checks_total += 1
    if check_file_exists('backend/app.py', 'Main Flask app'): checks_passed += 1
    
    checks_total += 1
    if check_file_exists('backend/routes/disease_routes.py', 'Disease routes'): checks_passed += 1
    
    checks_total += 1
    if check_file_exists('backend/routes/spread_routes.py', 'Spread routes'): checks_passed += 1
    
    checks_total += 1
    if check_file_exists('backend/services/database_service.py', 'Database service'): checks_passed += 1
    
    checks_total += 1
    if check_file_exists('backend/services/disease_service.py', 'Disease service'): checks_passed += 1
    
    checks_total += 1
    if check_file_exists('backend/services/spread_service.py', 'Spread service'): checks_passed += 1
    
    # Check frontend files
    print("\nFrontend Files:")
    checks_total += 1
    if check_file_exists('frontend/templates/index.html', 'Home page'): checks_passed += 1
    
    checks_total += 1
    if check_file_exists('frontend/templates/upload.html', 'Upload page'): checks_passed += 1
    
    checks_total += 1
    if check_file_exists('frontend/templates/map_dashboard.html', 'Map dashboard'): checks_passed += 1
    
    checks_total += 1
    if check_file_exists('frontend/static/css/style.css', 'CSS styles'): checks_passed += 1
    
    # Check ML models
    print("\nML Model Scripts:")
    checks_total += 1
    if check_file_exists('ml_models/train_disease_model.py', 'Disease model trainer'): checks_passed += 1
    
    checks_total += 1
    if check_file_exists('ml_models/train_spread_model.py', 'Spread model trainer'): checks_passed += 1
    
    # Check datasets
    print("\nDataset Files:")
    checks_total += 1
    if check_file_exists('datasets/generate_village_dataset.py', 'Dataset generator'): checks_passed += 1
    
    checks_total += 1
    if check_file_exists('datasets/village_dataset.csv', 'Village dataset'): checks_passed += 1
    
    # Check directories
    print("\nDirectories:")
    checks_total += 1
    if check_directory_exists('backend/models', 'Models directory'): checks_passed += 1
    
    checks_total += 1
    if check_directory_exists('backend/uploads', 'Uploads directory'): checks_passed += 1
    
    # Check requirements
    print("\nConfiguration Files:")
    checks_total += 1
    if check_file_exists('requirements.txt', 'Requirements file'): checks_passed += 1
    
    checks_total += 1
    if check_file_exists('README.md', 'README file'): checks_passed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"Results: {checks_passed}/{checks_total} checks passed")
    print("=" * 60)
    
    if checks_passed == checks_total:
        print("\n[SUCCESS] All checks passed! Setup looks good.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Train models (optional): cd ml_models && python train_spread_model.py")
        print("3. Run app: cd backend && python app.py")
    else:
        print(f"\n[WARNING] {checks_total - checks_passed} check(s) failed. Please review missing files.")
    
    return checks_passed == checks_total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
