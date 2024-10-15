import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class PlotWorker(QThread):
    finished = pyqtSignal(plt.Figure)  # Signal to emit when plotting is done

    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data

    def run(self):
        # Create Matplotlib plot
        fig, ax = plt.subplots()
        ax.plot(self.data['x'], self.data['y'])
        ax.set_xlabel("X Axis Label")
        ax.set_ylabel("Y Axis Label")
        ax.set_title("Plot from File")
        self.finished.emit(fig)  # Emit the figure

class DataPlotter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Plotter")
        self.data = None

        # Create UI elements
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.open_button = QPushButton("Open File")
        self.path_label = QLabel("No file selected.")
        self.error_label = QLabel("")
        self.canvas = None  # Canvas to hold the Matplotlib plot

        # Add elements to layout
        self.layout.addWidget(self.open_button)
        self.layout.addWidget(self.path_label)
        self.layout.addWidget(self.error_label)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        # Connect signals and slots
        self.open_button.clicked.connect(self.open_file_and_plot)

    def open_file_and_plot(self):
        # Open file dialog
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Select a File", "", "Text files (*.txt*);;All files (*.*)"
        )

        if filepath:
            self.path_label.setText(filepath)
            try:
                # Load data from the selected file
                self.data = pd.read_csv(
                    filepath, names=["x", "y"], skiprows=1, delimiter="\t"
                )

                self.worker = PlotWorker(self.data)
                self.worker.finished.connect(self.display_plot)
                self.worker.start()

            except Exception as e:
                self.error_label.setText(f"Error: {e}")

    def display_plot(self, fig):
        # Remove old canvas if it exists
        if self.canvas:
            self.layout.removeWidget(self.canvas)
            self.canvas.deleteLater()

        # Create canvas for Matplotlib figure
        self.canvas = FigureCanvas(fig)
        self.layout.addWidget(self.canvas)
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataPlotter()
    window.show()
    sys.exit(app.exec_())
