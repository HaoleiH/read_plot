import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QDialog, QInputDialog
from PyQt5.QtCore import QThread, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import csv
from matplotlib import rcParams
from cycler import cycler
# formatting the plots
def setup(ax):
    ax.xaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator(2))
rcParams['font.family'] = 'sans-serif'
#rcParams["font.family"] = "Times New Roman"
#rcParams['font.sans-serif'] = ['Arial']
rcParams['figure.figsize'] = [13.2, 10.2]
rcParams['axes.labelsize'] = 48
rcParams['axes.titlesize'] = 48
rcParams['xtick.labelsize'] = 36
rcParams['ytick.labelsize'] = 36
rcParams['axes.prop_cycle'] = cycler('color', ['#000000', '#FF0000', '#00FF00',
                                               '#0000FF','#00FFFF', '#FF00FF',
                                               '#FFFF00','#808000','#000080',
                                               '#800080','#800000','#008000',
                                               '#008080','#0000A0','#FF8000'])

#rcParams['text.usetex'] = True
rcParams['lines.linewidth'] = 4
rcParams['axes.linewidth'] = 3
rcParams['patch.linewidth'] = 0.48
rcParams['lines.markersize'] = 11.2
rcParams['lines.markeredgewidth'] = 0
rcParams['xtick.major.size'] = 8
rcParams['ytick.major.size'] = 8
rcParams['xtick.major.width'] = 3
rcParams['ytick.major.width'] = 3

rcParams['xtick.minor.visible'] = True
rcParams['xtick.minor.size'] = 6
rcParams['xtick.minor.width'] = 3
rcParams['ytick.minor.visible'] = True
rcParams['ytick.minor.size'] = 6
rcParams['ytick.minor.width'] = 3
#rcParams['ytick.minor.width'] = 0.8
rcParams['xtick.major.pad'] = 11.2
rcParams['ytick.major.pad'] = 11.2
#rcParams["xtick.top"] = True
rcParams['xtick.direction'] = "in"
rcParams['ytick.direction'] = "in"
rcParams['legend.frameon'] = False
rcParams['figure.autolayout'] = True

rcParams['legend.fontsize'] = 24


#axes.labelsize:     large  # font size of the x and y labels
##axes.labelpad:      4.0     # space between label and axis
#axes.labelweight:   normal  # weight of the x and y labels
#axes.labelcolor:    black


#axes.xmargin:   .1  # x margin.  See `axes.Axes.margins`
#axes.ymargin:   .2  # y margin.  See `axes.Axes.margins`
## Figure layout
#figure.autolayout: True  # When True, automatically adjust subplot
                           # parameters to make the plot fit the figure
                           # using `tight_layout`
#figure.constrained_layout.use: False  # When True, automatically make plot
                                       # elements fit on the figure. (Not
                                       # compatible with `autolayout`, above).
#figure.constrained_layout.h_pad:  0.04167  # Padding around axes objects. Float representing
#figure.constrained_layout.w_pad:  0.04167  # inches. Default is 3/72 inches (3 points)
#figure.constrained_layout.hspace: 0.02     # Space between subplot groups. Float representing
#figure.constrained_layout.wspace: 0.02     # a fraction of the subplot widths being separated.


class PlotWorker(QThread):
    finished = pyqtSignal(plt.Figure)

    def __init__(self, data_list, parent=None):
        super().__init__(parent)
        self.data_list = data_list

    def run(self):
        fig, ax = plt.subplots(figsize=(8, 8))
        for data in self.data_list:
            ax.plot(data['x'], data['y'])
        ax.set_xlabel("X Axis Label")
        ax.set_ylabel("Y Axis Label")
        #ax.set_title("Plot from Files")
        setup(ax)
        self.finished.emit(fig)

class DataPlotter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Plotter")
        self.setGeometry(100, 100, 1500, 1200)  # Adjusted size for toolbar
        self.data_list = []

        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.open_button = QPushButton("Open File")
        self.save_button = QPushButton("Save Plot")
        self.path_label = QLabel("No file selected.")
        self.error_label = QLabel("")
        self.canvas = None
        self.toolbar = None  # Add toolbar for interaction

        self.layout.addWidget(self.open_button)
        self.layout.addWidget(self.save_button)  # Add save button
        self.layout.addWidget(self.path_label)
        self.layout.addWidget(self.error_label)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.open_button.clicked.connect(self.open_file_and_plot)
        self.save_button.clicked.connect(self.save_plot)  # Connect save button

    def open_file_and_plot(self):
        filepaths, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Files",
            "/home/holyhigh/Documents/data",
            "Text files (*.txt*);;All files (*.*)"
        )

        if filepaths:
            self.path_label.setText("; ".join(filepaths))
            try:
                for filepath in filepaths:
                    with open(filepath, 'r') as f:
                        sniffer = csv.Sniffer()
                        dialect = sniffer.sniff(f.read(1024))  # Analyze the first 1024 bytes
                    data = pd.read_csv(
                        filepath, names=["x", "y"], skiprows=1, delimiter=dialect.delimiter
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
            self.layout.removeWidget(self.toolbar)  # Remove old toolbar
            self.canvas.deleteLater()
            self.toolbar.deleteLater()

        self.canvas = FigureCanvas(fig)
        self.toolbar = NavigationToolbar(self.canvas, self)  # Create toolbar
        self.layout.addWidget(self.toolbar)  # Add toolbar to layout
        self.layout.addWidget(self.canvas)
        self.canvas.draw()

    def save_plot(self):
        if self.canvas:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            filepath, _ = QFileDialog.getSaveFileName(self, "Save Plot As", "", "PNG (*.png);;JPEG (*.jpg *.jpeg);;PDF (*.pdf)", options=options)
            if filepath:
                self.canvas.figure.savefig(filepath,transparent=True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataPlotter()
    window.show()
    sys.exit(app.exec_())
