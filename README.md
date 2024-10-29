# StockAnalyzer Project

## Overview

**StockAnalyzer** is a Python project that analyzes financial data (such as stock prices) by sorting the data, identifying periods of maximum gain or loss, and detecting significant anomalies like price spikes or dips. The system implements algorithms such as Merge Sort, Kadane’s Algorithm, and the Closest Pair of Points algorithm to efficiently perform these tasks.

## Features

- **Data Loading**: Loads financial data from CSV files for analysis.
- **Sorting**: Uses Merge Sort to organize stock prices by date.
- **Gain/Loss Detection**: Detects periods of maximum gain or loss in stock prices.
- **Anomaly Detection**: Identifies anomalies such as large price changes within short timeframes.
- **Graphical Output**: Generates visual graphs of sorted data, gain/loss periods, and detected anomalies.

## Project Structure

```
StockAnalyzer/
├── data/               # CSV files for financial data
├── main.py             # Main script with all the analysis logic
└── README.md           # Project documentation
```

### Overall Structure and Flow

1. **Data Loading**: 
   - The `DataLoader` class is responsible for loading data from CSV files and preparing it for analysis.
   
2. **Sorting**:
   - The `MergeSort` class handles sorting the stock prices by date using the Merge Sort algorithm.
   
3. **Gain/Loss Detection**:
   - The `MaxSubarray` class identifies periods of maximum gain or loss by implementing Kadane’s Algorithm.
   
4. **Anomaly Detection**:
   - The `SpikeDipClosestPair` class detects significant anomalies using the Closest Pair of Points algorithm.

5. **Visualization**:
   - The program generates graphs to visualize the sorted data, the periods of maximum gain/loss, and any detected anomalies.

### Code Flow Diagram

```plaintext
  +-------------------+           +------------------+
  |    main.py        |           |    data/          |
  |  (Main Execution) |           |  (CSV Files)      |
  +--------+----------+           +------------------+
           |
           v
  +-------------------+
  |   DataLoader      |
  | (Loads CSV Data)  |
  +-------------------+
           |
           v
  +-------------------+
  |   MergeSort       | -----> Sorts the stock prices by date
  |  (Sorting)        |
  +-------------------+
           |
           v
  +-------------------+
  |   MaxSubarray     | -----> Identifies max gain/loss periods
  | (Gain/Loss)       |
  +-------------------+
           |
           v
  +-------------------+
  | SpikeDipClosest   | -----> Detects significant anomalies
  | (Anomaly Detection)|
  +-------------------+
           |
           v
  +-------------------+
  |   Visualization    | -----> Generates and displays graphs
  +-------------------+
```

## Algorithms Used

- **Merge Sort**: Sorts the stock prices by date for better analysis of trends and patterns.
- **Kadane’s Algorithm**: Finds the period with the maximum gain or loss by solving the maximum subarray problem.
- **Closest Pair of Points**: Detects significant anomalies such as sudden spikes or dips in stock prices.

## Setup Instructions

### Requirements

- Python 3.x
- Libraries: `pandas`, `matplotlib`, `numpy`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/StockAnalyzer.git
   ```

2. Navigate to the project directory:
   ```bash
   cd StockAnalyzer
   ```

3. Install the required Python libraries:
   ```bash
   pip install pandas matplotlib numpy
   ```

### Running the Project

1. Place your CSV stock data files inside the `data/` directory.
2. Run the main script:
   ```bash
   python main.py
   ```

### Example Usage

The program will load the financial data, sort the stock prices, detect the maximum gain/loss period, and find anomalies. Graphs will be generated and displayed after each step.

## Output

- **Sorted Data**: Displays a graph of sorted adjusted close prices.
- **Maximum Gain/Loss Period**: Highlights the period with the maximum gain or loss in stock prices.
- **Anomaly Detection**: Shows detected anomalies in the form of significant price spikes or dips.

## Example Graphs

### Sorted Stock Prices
![Sorted Stock Prices]()

### Maximum Gain/Loss Period
![Max Gain/Loss Period]()

### Anomaly Detection
![Anomalies Detected]()

## Diagrams and Explanation of Code Structure

The project follows a clear and modular structure, where each component has a well-defined role. Below is a diagram that explains the flow of the code:

1. **DataLoader**:
   - Loads stock data from CSV files and processes it for further analysis.
   
2. **MergeSort**:
   - Sorts the stock data by date to allow for more efficient trend analysis.

3. **MaxSubarray**:
   - Detects the period with the largest gain or loss in stock prices using Kadane's Algorithm.

4. **SpikeDipClosestPair**:
   - Finds anomalies by calculating sudden price changes over short periods.

5. **Visualization**:
   - The program generates various graphs for the sorted data, gain/loss periods, and anomalies.

Each class is designed with clear separation of concerns to ensure that the code is maintainable and extensible. The diagrams and modular design help explain how each part interacts and fits together.
