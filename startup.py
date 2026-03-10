import os
import sys
import winshell
from win32com.client import Dispatch

def create_startup_shortcut():
    """Creates a shortcut in the Windows Startup folder to run the app hiddenly."""
    startup_path = winshell.startup()
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the VBS wrapper (to hide the CMD window)
    vbs_path = os.path.join(project_root, "run_verbatim.vbs")
    
    # Create the VBS script if it doesn't exist
    vbs_content = f'''Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "{project_root}\\venv\\Scripts\\python.exe {project_root}\\main.py", 0
Set WshShell = Nothing
'''
    with open(vbs_path, "w") as vbs:
        vbs.write(vbs_content)
        
    # Create shortcut in Startup folder
    shortcut_path = os.path.join(startup_path, "Verbatim.lnk")
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = "wscript.exe"
    shortcut.Arguments = f'"{vbs_path}"'
    shortcut.IconLocation = os.path.join(project_root, "main.py") # Temporary icon ref
    shortcut.WorkingDirectory = project_root
    shortcut.save()
    
    print(f"Startup shortcut created at: {shortcut_path}")

if __name__ == "__main__":
    create_startup_shortcut()
