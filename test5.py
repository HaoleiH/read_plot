# able to start from certain dir
import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class PlotWorker(QThread):
    finished = pyqtSignal(plt.Figure)

    def __init__(self, data_list, parent=None):
        super().__init__(parent)
        self.data_list = data_list

    def run(self):
        fig, ax = plt.subplots()
        for data in self.data_list:
            ax.plot(data['x'], data['y'])
        ax.set_xlabel("X Axis Label")
        ax.set_ylabel("Y Axis Label")
        ax.set_title("Plot from Files")
        self.finished.emit(fig)

class DataPlotter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Plotter")
        self.setGeometry(100, 100, 600, 600)
        self.data_list = []

        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.open_button = QPushButton("Open File")
        self.path_label = QLabel("No file selected.")
        self.error_label = QLabel("")
        self.canvas = None

        self.layout.addWidget(self.open_button)
        self.layout.addWidget(self.path_label)
        self.layout.addWidget(self.error_label)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.open_button.clicked.connect(self.open_file_and_plot)

    def open_file_and_plot(self):
        filepaths, _ = QFileDialog.getOpenFileNames(
            self, 
            "Select Files", 
            "/home/holyhigh/Documents/data",  # Set default directory here
            "Text files (*.txt*);;All files (*.*)"
        )

        if filepaths:
            self.path_label.setText("; ".join(filepaths))
            try:
                for filepath in filepaths:
                    data = pd.read_csv(
                        filepath, names=["x", "y"], skiprows=1, delimiter="\t"
                    )
                    self.data_list.append(data)

                self.worker = PlotWorker(self.data_list)
                self.worker.finished.connect(self.display_plot)
                self.worker.start()

            except Exception as e:
                self.error_label.setText(f"Error: {e}")

    def display_plot(self, fig):
        if self.canvas:
            self.layout.removeWidget(self.canvas)
            self.canvas.deleteLater()

        self.canvas = FigureCanvas(fig)
        self.layout.addWidget(self.canvas)
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataPlotter()
    window.show()
    sys.exit(app.exec_())
