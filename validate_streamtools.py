import subprocess
import sys
import api.controlcenter.st_settings as s
from tkinter import messagebox


def install_requirements(requirements_file):
    """
    Install missing requirements using pip
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to install requirements. Error message: {e}")
        sys.exit(1)


# Check if requirements are installed
missing_requirements = []
for requirement in open(s.config['requirements_file'], 'r').readlines():
    requirement = requirement.strip()
    try:
        __import__(requirement)
    except ImportError:
        missing_requirements.append(requirement)

# Install missing requirements with pip
if missing_requirements:
    prompt = f"The following requirements are missing: {', '.join(missing_requirements)}\n\nDo you want to install them now?"
    if messagebox.askyesno("Missing Requirements", prompt):
        install_requirements(s.config['requirements_file'])

        # Check if requirements are installed
        missing_requirements = []
        for requirement in open(s.config['requirements_file'], 'r').readlines():
            requirement = requirement.strip()
            try:
                __import__(requirement)
            except ImportError:
                missing_requirements.append(requirement)

        if missing_requirements:
            messagebox.showerror("Error", f"Failed to install the following requirements: {', '.join(missing_requirements)}. Please install them manually.")
            sys.exit(1)

print("All requirements are installed.")
sys.exit(0)
