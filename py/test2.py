import pandas as pd
import plotly.express as px
import tkinter as tk
from tkinter import filedialog
from plotly.offline import plot

# Function to open file dialog and update plot
def open_file_and_plot():
    global data, fig  # Access global variables

    # Open file dialog
    filepath = filedialog.askopenfilename(
        initialdir="/",
        title="Select a File",
        filetypes=(("Text files", "*.txt*"), ("all files", "*.*")),
    )

    # Update the path label
    path_label.config(text=filepath)

    try:
        # Load data from the selected file
        data = pd.read_csv(filepath, names=["x", "y"], skiprows=1, delimiter="\t")

        # Create or update the plot
        fig = px.scatter(data, x="x", y="y", title="Plot from File")
        fig.update_layout(xaxis_title="X Axis Label", yaxis_title="Y Axis Label")

        # Display the plot in the browser (or use fig.show() for a separate window)
        plot(fig)

    except Exception as e:
        # Handle errors (e.g., file not found, invalid format)
        error_label.config(text=f"Error: {e}")

# Create main window
root = tk.Tk()
root.title("Data Plotter")

# Button to open file dialog
open_button = tk.Button(root, text="Open File", command=open_file_and_plot)
open_button.pack(pady=20)

# Label to display selected file path
path_label = tk.Label(root, text="No file selected.")
path_label.pack()

# Label to display potential errors
error_label = tk.Label(root, text="", fg="red")
error_label.pack()

# Initialize global variables for data and plot
data = None
fig = None

# Run the Tkinter event loop
root.mainloop()
