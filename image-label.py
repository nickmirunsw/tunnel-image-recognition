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

# Prepare CSV file for saving labels
if not os.path.exists(output_csv):
    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Image", "Software", "Output_Type", "Num_Tunnels", "Crown_Value", "Sidewall_Value", "Tunnel_Shape"])

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
        self.num_tunnels_label = tk.Label(master, text="Number of Tunnels:")
        self.num_tunnels_label.pack()
        self.num_tunnels_entry = tk.Entry(master)
        self.num_tunnels_entry.pack()

        # **Value at Crown Entry**
        self.crown_label = tk.Label(master, text="Value at Crown (leave empty if N/A):")
        self.crown_label.pack()
        self.crown_entry = tk.Entry(master)
        self.crown_entry.pack()

        # **Value at Sidewall Entry**
        self.sidewall_label = tk.Label(master, text="Value at Sidewalls (leave empty if N/A):")
        self.sidewall_label.pack()
        self.sidewall_entry = tk.Entry(master)
        self.sidewall_entry.pack()

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
        self.save_button.pack(pady=10)

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
        num_tunnels = self.num_tunnels_entry.get()
        crown_value = self.crown_entry.get().strip()
        sidewall_value = self.sidewall_entry.get().strip()
        selected_shape = self.shape_var.get()

        # Set "N/A" if values are empty
        if not crown_value:
            crown_value = "N/A"
        if not sidewall_value:
            sidewall_value = "N/A"

        with open(output_csv, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                self.image_files[self.image_index], selected_software, selected_output, 
                num_tunnels, crown_value, sidewall_value, selected_shape
            ])

        self.image_index += 1
        self.clear_inputs()
        self.load_image()

    def clear_inputs(self):
        """Clear input fields for next entry."""
        self.software_var.set("")
        self.output_var.set("")
        self.num_tunnels_entry.delete(0, tk.END)
        self.crown_entry.delete(0, tk.END)
        self.sidewall_entry.delete(0, tk.END)
        self.shape_var.set("")

# Run GUI
root = tk.Tk()
app = ImageLabelingApp(root)
root.mainloop()
