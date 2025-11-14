# Exocet - Protium-2500 Fuel Cell Controller

Exocet is a web-based application for monitoring and controlling a Protium-2500 fuel cell. It provides a user-friendly interface built with Streamlit to manage the fuel cell's operations and view real-time data.

## Features

- **Serial Port Connection:** Easily connect to and disconnect from the fuel cell via a specified COM port.
- **Fuel Cell Control:** Start and stop the fuel cell, and control components like fans and blowers.
- **Real-time Monitoring:** View live data streams and raw messages from the fuel cell.
- **Data Persistence:** Utilizes QuestDB, a high-performance time-series database, for data storage.

## Requirements

- Python 3.13+
- A Protium-2500 Fuel Cell

## Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/lirei-uqtr/exocet.git
    cd exocet
    ```

2.  **Install Python dependencies:**
    It is recommended to use a virtual environment. `uv` is used for package management.
    ```bash
    # Install dependencies from pyproject.toml
    uv sync
    ```


## Usage

1.  **Run the Streamlit application:**
    ```bash
    streamlit run src/app.py
    ```

2.  **Connect to the Fuel Cell:**
    - Open your web browser to the local URL provided by Streamlit.
    - Enter the COM port your fuel cell is connected to (e.g., `COM7`).
    - Click "Connect".

3.  **Control and Monitor:**
    - Use the sidebar commands to operate the fuel cell.
    - View real-time data and raw messages in the main dashboard.

## Data Analysis

### Polarization Curve

To generate a polarization curve from a CSV data file, run the `plot_polarization.py` script.

```bash
python src/plot_polarization.py
```

This will create a `polarization_curve.png` file in the root of the project. You can customize the input file, active area, and output file name using command-line arguments:

```bash
python src/plot_polarization.py --file path/to/your/data.csv --area 125.0 --output my_plot.png
```

## Project Structure

```
.
├── data/                  # Contains data files (e.g., CSVs)
├── docs/                  # Documentation
├── src/                   # Source code
│   ├── app.py             # Main Streamlit application
│   ├── fuel_cell_controller.py # Logic for fuel cell communication
│   └── plot_polarization.py # Script to plot polarization curves
├── .gitignore             # Files to ignore in Git
├── pyproject.toml         # Project metadata and dependencies
└── README.md              # This file