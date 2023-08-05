import hashlib
import os
import tkinter as tk
from tkinter import filedialog

def sanitize_file_path(file_path):
    # Replace any backslashes with forward slashes
    sanitized_path = file_path.strip().replace("\\", "/")
    return sanitized_path.replace("\\\\", "/")

def calculate_checksum(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read the file in chunks
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def browse_file():
    # Open window to select file
    file_path = filedialog.askopenfilename()
    if file_path:
        # Clear any previous data and replace with new data (filepath)
        file_path_entry.delete(0, tk.END)
        file_path_entry.insert(0, file_path)

def calculate_checksum_gui():
    # Load filepath into variable
    user_input_file = file_path_entry.get().strip()

    if not user_input_file:
        checksum_file_var.set("Please provide a valid file path.")
        checksum_optional_var.set("SHA-256 Checksum (Comparitor):")
        comparison_label.config(text="INVALID", fg="black")
        comparison_label.bind("<Enter>", lambda event: show_tooltip("There is currently no checksum to compare to."))
        comparison_label.bind("<Leave>", hide_tooltip)
        return

    sanitized_path = sanitize_file_path(user_input_file)
    if not os.path.exists(sanitized_path):
        checksum_file_var.set("File not found. Please enter a valid file path.")
        checksum_optional_var.set("SHA-256 Checksum (Comparitor):")
        comparison_label.config(text="INVALID", fg="black")
        comparison_label.bind("<Enter>", lambda event: show_tooltip("There is currently no checksum to compare to."))
        comparison_label.bind("<Leave>", hide_tooltip)
        return

    checksum_file = calculate_checksum(sanitized_path)

    user_input_optional_checksum = optional_checksum_entry.get().strip()
    checksum_optional = user_input_optional_checksum

    # Ensure both checksums have the same length by adding spaces to the shorter one
    max_len = max(len(checksum_file), len(checksum_optional))
    checksum_file_aligned = checksum_file.ljust(max_len)
    checksum_optional_aligned = checksum_optional.ljust(max_len)

    # Clear any previous text
    checksum_file_label.delete(1.0, tk.END)
    checksum_optional_label.delete(1.0, tk.END)

    # Clear any previous tags
    checksum_file_label.tag_delete("file_match", "file_no_match")
    checksum_optional_label.tag_delete("optional_match", "optional_no_match")

    # Set font to monospaced
    checksum_file_label.config(font=("Courier New", 12))
    checksum_optional_label.config(font=("Courier New", 12))

    # Compare each symbol and apply color tags accordingly
    for i, (symbol_file, symbol_optional) in enumerate(zip(checksum_file_aligned, checksum_optional_aligned)):
        tag_name_file = "file_match" if symbol_file == symbol_optional else "file_no_match"
        tag_name_optional = "optional_match" if symbol_optional and symbol_file == symbol_optional else "optional_no_match"

        checksum_file_label.insert(tk.END, symbol_file, tag_name_file)
        checksum_optional_label.insert(tk.END, symbol_optional, tag_name_optional)

    # Set the color tags for matched and unmatched symbols
    checksum_file_label.tag_config("file_match", foreground="green")
    checksum_file_label.tag_config("file_no_match", foreground="red")
    checksum_optional_label.tag_config("optional_match", foreground="green")
    checksum_optional_label.tag_config("optional_no_match", foreground="red")
    #^ These variables should be combined

    # Show the aligned checksums
    checksum_file_label.pack()
    checksum_optional_label.pack()

    # Compare the checksums and display the result at the bottom
    if not checksum_optional:
        comparison_label.config(text="INVALID", fg="black")
        comparison_label.bind("<Enter>", lambda event: show_tooltip("There is currently no checksum to compare to."))
        comparison_label.bind("<Leave>", hide_tooltip)
    elif checksum_file == checksum_optional:
        comparison_label.config(text="MATCH", fg="green")
        comparison_label.bind("<Enter>", lambda event: show_tooltip("The file checksum matches the supplied checksum."))
        comparison_label.bind("<Leave>", hide_tooltip)
    else:
        comparison_label.config(text="MISMATCH", fg="red")
        comparison_label.bind("<Enter>", lambda event: show_tooltip("The file checksum does not match the supplied checksum."))
        comparison_label.bind("<Leave>", hide_tooltip)

# Function to show tooltip
def show_tooltip(tooltip_text):
    tooltip_label.config(text=tooltip_text, fg="white")

# Function to hide tooltip
def hide_tooltip(event):
    tooltip_label.config(text="")

# Create the main Tkinter window
root = tk.Tk()
root.title("SHA-256 Checksum Calculator")

# Create a bold title banner
title_banner = tk.Label(root, text="SHA-256 Checksum Checker", font=("Arial", 24, "bold"))
title_banner.pack(pady=5)
dev_label = tk.Label(root, text="Open Sourced by RawVendetta", font=("Arial", 8, "italic"))
dev_label.pack(pady=10)

# Create a label and an entry field for the file path
file_path_label = tk.Label(root, text="Enter the file path:")
file_path_label.pack(pady=2)
file_path_entry = tk.Entry(root)
file_path_entry.pack(fill=tk.X, padx=10)

# Create a button to browse for the file
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack(pady=5)

# Create a label and an entry field for the optional checksum
optional_checksum_label = tk.Label(root, text="Enter the optional checksum (if available):")
optional_checksum_label.pack(pady=2)
optional_checksum_entry = tk.Entry(root)
optional_checksum_entry.pack(fill=tk.X, padx=10)

# Create a button to calculate the checksum
calculate_button = tk.Button(root, text="Calculate Checksum", command=calculate_checksum_gui)
calculate_button.pack(pady=10)

# Create labels to display the checksum results
checksum_file_var = tk.StringVar()
checksum_file_label = tk.Text(root, height=1, wrap="none", font=("Courier New", 12), relief=tk.FLAT)
checksum_file_label.pack()

checksum_optional_var = tk.StringVar()
checksum_optional_label = tk.Text(root, height=1, wrap="none", font=("Courier New", 12), relief=tk.FLAT)
checksum_optional_label.pack()

# Create a label to display the comparison result
comparison_label = tk.Label(root, text="", font=("Arial", 16, "bold"))
comparison_label.pack()

# Create a label to display the tooltip
tooltip_label = tk.Label(root, text="", font=("Arial", 12), bg="black", fg="white", relief=tk.SOLID)
tooltip_label.pack(fill=tk.X)

# Start the Tkinter event loop
root.mainloop()
