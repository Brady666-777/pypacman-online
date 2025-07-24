#!/usr/bin/env python3
"""
Setup script for PyPacman Multiplayer
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing PyPacman Multiplayer requirements...")
    
    try:
        # Install pygame
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pygame>=2.0.0'])
        print("✓ pygame installed")
        
        # Install pygame-menu
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pygame-menu>=4.0.0'])
        print("✓ pygame-menu installed")
        
        print("\n✓ All requirements installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing requirements: {e}")
        return False

def check_assets():
    """Check if game assets exist"""
    print("Checking game assets...")
    
    asset_dirs = [
        'assets/sounds',
        'assets/ghosts',
        'assets/pacman-up',
        'assets/pacman-down',
        'assets/pacman-left',
        'assets/pacman-right',
        'levels'
    ]
    
    missing = []
    for asset_dir in asset_dirs:
        if not os.path.exists(asset_dir):
            missing.append(asset_dir)
    
    if missing:
        print("⚠ Missing asset directories:")
        for m in missing:
            print(f"  - {m}")
        print("The game may not work correctly without these assets.")
        return False
    else:
        print("✓ All asset directories found")
        return True

def create_directories():
    """Create necessary directories"""
    print("Creating directories...")
    
    dirs_to_create = [
        'server',
        'client', 
        'multiplayer',
        'logs'
    ]
    
    for dir_name in dirs_to_create:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"✓ Created directory: {dir_name}")

def main():
    """Main setup function"""
    print("PyPacman Multiplayer Setup")
    print("=" * 30)
    
    # Create directories
    create_directories()
    
    # Install requirements
    if not install_requirements():
        print("Setup failed due to installation errors.")
        return False
    
    # Check assets
    assets_ok = check_assets()
    
    print("\n" + "=" * 30)
    if assets_ok:
        print("✓ Setup completed successfully!")
        print("\nYou can now run the game with:")
        print("  python main_multiplayer.py")
        print("\nOr use the launcher:")
        print("  launcher.bat (Windows)")
    else:
        print("⚠ Setup completed with warnings.")
        print("Please ensure all asset files are in place.")
    
    return True

if __name__ == "__main__":
    main()
