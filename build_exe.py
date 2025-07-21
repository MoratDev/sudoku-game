"""
Build script to create executable file using cx_Freeze or PyInstaller
"""
import os
import subprocess
import sys

def build_with_pyinstaller():
    """Build executable using PyInstaller"""
    try:
        # Install PyInstaller if not available
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        
        # Build command
        cmd = [
            "pyinstaller",
            "--onefile",  # Single executable file
            "--windowed",  # No console window (for GUI)
            "--name", "SudokuGame",
            "--icon", "icon.ico",  # Add icon if available
            "sudoku_pygame.py"
        ]
        
        # Remove icon option if file doesn't exist
        if not os.path.exists("icon.ico"):
            cmd.remove("--icon")
            cmd.remove("icon.ico")
        
        print("Building executable with PyInstaller...")
        subprocess.check_call(cmd)
        
        print("\n✅ Executable built successfully!")
        print("📁 Find your executable in the 'dist' folder")
        print("🎮 Executable name: SudokuGame.exe (Windows) or SudokuGame (Mac/Linux)")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error building executable: {e}")
        return False
    
    return True

def build_with_cxfreeze():
    """Alternative build method using cx_Freeze"""
    try:
        # Install cx_Freeze if not available
        subprocess.check_call([sys.executable, "-m", "pip", "install", "cx_freeze"])
        
        # Create setup script for cx_Freeze
        cx_setup_content = '''
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_options = {
    'packages': ['pygame', 'copy', 'random'],
    'excludes': [],
    'include_files': []
}

base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('sudoku_pygame.py', base=base, target_name='SudokuGame')
]

setup(
    name='SudokuGame',
    version='1.0.0',
    description='Sudoku Game with Pygame',
    options={'build_exe': build_options},
    executables=executables
)
'''
        
        with open("setup_cx.py", "w") as f:
            f.write(cx_setup_content)
        
        print("Building executable with cx_Freeze...")
        subprocess.check_call([sys.executable, "setup_cx.py", "build"])
        
        print("\n✅ Executable built successfully with cx_Freeze!")
        print("📁 Find your executable in the 'build' folder")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error building with cx_Freeze: {e}")
        return False
    
    return True

def main():
    print("🏗️  Sudoku Game Executable Builder")
    print("="*50)
    
    print("\nChoose build method:")
    print("1. PyInstaller (Recommended)")
    print("2. cx_Freeze (Alternative)")
    print("3. Both methods")
    
    try:
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            build_with_pyinstaller()
        elif choice == "2":
            build_with_cxfreeze()
        elif choice == "3":
            print("\n🔨 Building with PyInstaller first...")
            success1 = build_with_pyinstaller()
            print("\n🔨 Building with cx_Freeze...")
            success2 = build_with_cxfreeze()
            
            if success1 or success2:
                print("\n✅ At least one build method succeeded!")
        else:
            print("❌ Invalid choice. Please run the script again.")
    
    except KeyboardInterrupt:
        print("\n👋 Build cancelled by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()