import pandas as pd
import plotly.express as px

# Load data from a CSV file
data = pd.read_csv("/home/holyhigh/Documents/data/PLRaman/06190621/0619Si01_Pl_5pct_P1.txt",names=["x","y"],skiprows=1,delimiter="\t")  # Replace "your_data.csv" with your file name

# Create a scatter plot
fig = px.scatter(data, x="x", y="y", title="Your Plot Title")

# Customize the plot (optional)
fig.update_layout(xaxis_title="X Axis Label", yaxis_title="Y Axis Label")

# Show the plot
fig.show()
