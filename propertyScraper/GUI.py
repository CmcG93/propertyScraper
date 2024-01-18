import tkinter as tk
import subprocess
import os

def activate_venv():
    venv_activation_command = "source venv/bin/activate" if os.name != 'nt' else "venv/Scripts/activate"
    subprocess.run(venv_activation_command, shell=True)

def run_for_sale_script():
    activate_venv()
    subprocess.run(["python", "propertyForSaleScrape.py"])

def run_for_rent_script():
    activate_venv()
    subprocess.run(["python", "propertyForRentScrape.py"])

# Create the main window
root = tk.Tk()
root.title("Property Scraper")

# Create a header label
header_label = tk.Label(root, text="Irish Property Scraper", font=("Helvetica", 16, "bold"))
header_label.pack(pady=10)

# Create buttons for "For Sale" and "For Rent"
for_sale_button = tk.Button(root, text="For Sale", command=run_for_sale_script)
for_sale_button.pack(side="left", padx=10, pady=10)

for_rent_button = tk.Button(root, text="For Rent", command=run_for_rent_script)
for_rent_button.pack(side="right", padx=10, pady=10)

# Start the main loop
root.mainloop()
