"""
Image Labeling Tool for Tunnel Displacement Analysis

This script provides a graphical user interface (GUI) using Tkinter to label tunnel displacement images.
Users can input values for vertical and horizontal displacements at multiple tunnel locations.
The data is saved into a CSV file for further processing.

Features:
- Loads images from a directory
- Allows labeling for vertical and horizontal displacement (up to 4 tunnels)
- Automatically fills missing values as "N/A"
- Saves labeled data into `manual_labels.csv`
- Skips already labeled images to avoid duplication
- Provides a "Skip" button to move past images without labeling

Required Modules:
- tkinter
- cv2 (OpenCV)
- PIL (Pillow)
- os
- csv

Installation:
Run the following command to install the required modules:

pip install opencv-python pillow

Author: Nick Mirsepassi
Date: 23/02/2025

"""


import tkinter as tk
import cv2
from PIL import Image, ImageTk
import os
import csv

# Define paths
image_folder = "extracted-images"
output_csv = "manual_labels.csv"

# Get list of images
image_files = []
for root, _, files in os.walk(image_folder):
    for file in files:
        if file.endswith((".png", ".jpg", ".jpeg")):
            image_files.append(os.path.join(root, file))

# Load already labeled images to avoid duplicates
labeled_images = set()
if os.path.exists(output_csv):
    with open(output_csv, "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        for row in reader:
            labeled_images.add(row[0])  # First column contains image paths

# Remove already labeled images from the list
image_files = [img for img in image_files if img not in labeled_images]

# Prepare CSV file for saving labels
if not os.path.exists(output_csv):
    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Image", "Software", "Output_Type", "Num_Tunnels",
            "Crown_T1", "Crown_T2", "Crown_T3", "Crown_T4",
            "Sidewall_Left_T1", "Sidewall_Left_T2", "Sidewall_Left_T3", "Sidewall_Left_T4",
            "Sidewall_Right_T1", "Sidewall_Right_T2", "Sidewall_Right_T3", "Sidewall_Right_T4",
            "Tunnel_Shape"
        ])

# GUI Application
class ImageLabelingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Labeling Tool")

        # Load first image
        self.image_index = 0
        self.image_files = image_files
        self.current_image = None

        # Create UI components
        self.label = tk.Label(master, text="Classify Image:")
        self.label.pack()

        self.canvas = tk.Canvas(master, width=600, height=400)
        self.canvas.pack()

        # **Software Output Dropdown**
        self.software_label = tk.Label(master, text="Select Software Output:")
        self.software_label.pack()
        self.software_var = tk.StringVar()
        self.software_dropdown = tk.OptionMenu(
            master, self.software_var, 
            "RS2", "RS3", "PLAXIS2D", "PLAXIS3D", "UDEC", "FLAC2D", "FLAC3D", "3DEC"
        )
        self.software_dropdown.pack()

        # **Output Type Dropdown**
        self.output_label = tk.Label(master, text="Select Output Type:")
        self.output_label.pack()
        self.output_var = tk.StringVar()
        self.output_dropdown = tk.OptionMenu(
            master, self.output_var, 
            "Model", "Vertical Displacement", "Horizontal Displacement", "Stress Distribution", 
            "Bolt Axial Load", "Shear"
        )
        self.output_dropdown.pack()

        # **Number of Tunnels Entry**
        self.num_tunnels_label = tk.Label(master, text="Number of Tunnels (1-4):")
        self.num_tunnels_label.pack()
        self.num_tunnels_entry = tk.Entry(master)
        self.num_tunnels_entry.pack()

        # **Row for Vertical Displacement (Crown Values)**
        self.crown_frame = tk.Frame(master)
        self.crown_frame.pack(pady=5)
        tk.Label(self.crown_frame, text="(Crown Values):").grid(row=0, column=0, columnspan=5)

        self.crown_entries = []
        for i in range(4):
            tk.Label(self.crown_frame, text=f"Tunnel {i+1}").grid(row=1, column=i)
            entry = tk.Entry(self.crown_frame, width=10)
            entry.grid(row=2, column=i)
            self.crown_entries.append(entry)

        # **Row for Horizontal Displacement (Sidewall Left)**
        self.sidewall_left_frame = tk.Frame(master)
        self.sidewall_left_frame.pack(pady=5)
        tk.Label(self.sidewall_left_frame, text="(Sidewall Left):").grid(row=0, column=0, columnspan=5)

        self.sidewall_left_entries = []
        for i in range(4):
            tk.Label(self.sidewall_left_frame, text=f"Tunnel {i+1}").grid(row=1, column=i)
            entry = tk.Entry(self.sidewall_left_frame, width=10)
            entry.grid(row=2, column=i)
            self.sidewall_left_entries.append(entry)

        # **Row for Horizontal Displacement (Sidewall Right)**
        self.sidewall_right_frame = tk.Frame(master)
        self.sidewall_right_frame.pack(pady=5)
        tk.Label(self.sidewall_right_frame, text="(Sidewall Right):").grid(row=0, column=0, columnspan=5)

        self.sidewall_right_entries = []
        for i in range(4):
            tk.Label(self.sidewall_right_frame, text=f"Tunnel {i+1}").grid(row=1, column=i)
            entry = tk.Entry(self.sidewall_right_frame, width=10)
            entry.grid(row=2, column=i)
            self.sidewall_right_entries.append(entry)

        # **Tunnel Shape Dropdown**
        self.shape_label = tk.Label(master, text="Select Tunnel Shape:")
        self.shape_label.pack()
        self.shape_var = tk.StringVar()
        self.shape_dropdown = tk.OptionMenu(
            master, self.shape_var, "Arch", "Circular", "Rectangular", "Other"
        )
        self.shape_dropdown.pack()

        # **Save Button**
        self.save_button = tk.Button(master, text="Save Label", command=self.save_label)
        self.save_button.pack(pady=5)

        # **Skip Button**
        self.skip_button = tk.Button(master, text="Skip Image", command=self.skip_image)
        self.skip_button.pack(pady=5)

        self.load_image()

    def load_image(self):
        """Load and display the next image."""
        if self.image_index >= len(self.image_files):
            self.label.config(text="All images classified!")
            return

        image_path = self.image_files[self.image_index]
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (600, 400))

        self.current_image = Image.fromarray(image)
        self.tk_image = ImageTk.PhotoImage(self.current_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

        self.label.config(text=f"Classify Image: {os.path.basename(image_path)}")

    def save_label(self):
        """Save the label for the current image and load the next one."""
        selected_software = self.software_var.get()
        selected_output = self.output_var.get()
        num_tunnels = self.num_tunnels_entry.get().strip() or "N/A"
        selected_shape = self.shape_var.get()

        # Collect tunnel values, defaulting to "N/A" if blank
        crown_values = [entry.get().strip() or "N/A" for entry in self.crown_entries]
        sidewall_left_values = [entry.get().strip() or "N/A" for entry in self.sidewall_left_entries]
        sidewall_right_values = [entry.get().strip() or "N/A" for entry in self.sidewall_right_entries]

        with open(output_csv, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                self.image_files[self.image_index], selected_software, selected_output, num_tunnels,
                *crown_values, *sidewall_left_values, *sidewall_right_values, selected_shape
            ])

        self.image_index += 1
        self.clear_inputs()
        self.load_image()

    def skip_image(self):
        """Skip the current image and move to the next one."""
        self.image_index += 1
        self.load_image()

    def clear_inputs(self):
        """Clear input fields for next entry."""
        self.software_var.set("")
        self.output_var.set("")
        self.num_tunnels_entry.delete(0, tk.END)
        for entry in self.crown_entries + self.sidewall_left_entries + self.sidewall_right_entries:
            entry.delete(0, tk.END)
        self.shape_var.set("")

# Run GUI
root = tk.Tk()
app = ImageLabelingApp(root)
root.mainloop()
