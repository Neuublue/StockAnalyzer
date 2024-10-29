import pandas as pd
import numpy as np
import os
from datetime import datetime
import matplotlib.pyplot as plt

# DataLoader: Responsible for loading and merging financial datasets
class DataLoader:
    def __init__(self, file_paths):
        self.file_paths = [os.path.join('stock_data', file) for file in file_paths] if isinstance(file_paths, list) else [os.path.join('stock_data', file_paths)]
        self.data = None

    def load_data(self):
        # Verify files and load the data
        if not all(os.path.exists(file) for file in self.file_paths):
            raise FileNotFoundError("One or more files not found.")
        
        data_frames = [self._read_and_format(file) for file in self.file_paths]
        if len(data_frames) > 1:
            self.data = self._merge_data(data_frames)
        else:
            self.data = data_frames[0]
        print("Data loaded successfully.")
        return self.data

    def _read_and_format(self, file_path):
        # Helper method to load and format a CSV
        data = pd.read_csv(file_path)
        data['Date'] = pd.to_datetime(data['Date'], dayfirst=True)
        return data

    def _merge_data(self, data_frames):
        # Helper method to merge multiple datasets on 'Date'
        merged_data = data_frames[0]
        for df in data_frames[1:]:
            merged_data = pd.merge(merged_data, df, on='Date', how='inner')
        return merged_data

# MergeSort: Implements Merge Sort to handle large-scale sorting
class MergeSort:
    def __init__(self, key_column):
        self.key_column = key_column

    def sort(self, data):
        data_list = data.to_dict('records')
        sorted_data = self._merge_sort(data_list)
        return pd.DataFrame(sorted_data)

    def _merge_sort(self, arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left_sorted = self._merge_sort(arr[:mid])
        right_sorted = self._merge_sort(arr[mid:])
        return self._merge(left_sorted, right_sorted)

    def _merge(self, left, right):
        sorted_list = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i][self.key_column] <= right[j][self.key_column]:
                sorted_list.append(left[i])
                i += 1
            else:
                sorted_list.append(right[j])
                j += 1
        sorted_list.extend(left[i:])
        sorted_list.extend(right[j:])
        return sorted_list

# MaxSubarray: Identifies periods of maximum gain or loss
class MaxSubarray:
    @staticmethod
    def find_max_gain(prices):
        price_changes = [prices[i+1] - prices[i] for i in range(len(prices) - 1)]
        return MaxSubarray._max_subarray_sum(price_changes, 0, len(price_changes) - 1)

    @staticmethod
    def _max_subarray_sum(arr, low, high):
        if low == high:
            return arr[low], low, high
        mid = (low + high) // 2
        left_sum, left_start, left_end = MaxSubarray._max_subarray_sum(arr, low, mid)
        right_sum, right_start, right_end = MaxSubarray._max_subarray_sum(arr, mid + 1, high)
        cross_sum = MaxSubarray._max_crossing_sum(arr, low, mid, high)
        if left_sum >= right_sum and left_sum >= cross_sum:
            return left_sum, left_start, left_end
        elif right_sum >= left_sum and right_sum >= cross_sum:
            return right_sum, right_start, right_end
        else:
            return cross_sum, left_start, right_end

    @staticmethod
    def _max_crossing_sum(arr, low, mid, high):
        left_sum = total = float('-inf')
        for i in range(mid, low - 1, -1):
            total += arr[i]
            left_sum = max(left_sum, total)
        right_sum = total = float('-inf')
        for i in range(mid + 1, high + 1):
            total += arr[i]
            right_sum = max(right_sum, total)
        return left_sum + right_sum

# SpikeDipClosestPair: Detects anomalies in price changes
class SpikeDipClosestPair:
    @staticmethod
    def find_all_significant_spikes_dips(prices, threshold):
        prices.sort(key=lambda point: point[0])  # Sort by date
        return SpikeDipClosestPair._find_all_changes_rec(prices, threshold)

    @staticmethod
    def _find_all_changes_rec(prices, threshold):
        n = len(prices)
        if n <= 3:
            return SpikeDipClosestPair._brute_force(prices, threshold)
        mid = n // 2
        left_changes = SpikeDipClosestPair._find_all_changes_rec(prices[:mid], threshold)
        right_changes = SpikeDipClosestPair._find_all_changes_rec(prices[mid:], threshold)
        return left_changes + right_changes + SpikeDipClosestPair._strip_collect_significant_changes(prices, mid, threshold)

    @staticmethod
    def _strip_collect_significant_changes(prices, mid, threshold):
        # Method to find changes in a narrow strip
        strip = [price for price in prices if abs((price[0] - prices[mid][0]).days) < 10]
        return SpikeDipClosestPair._brute_force(strip, threshold)

    @staticmethod
    def _brute_force(prices, threshold):
        # Brute force method for smaller data
        significant_changes = []
        for i in range(len(prices)):
            for j in range(i + 1, len(prices)):
                days_apart = abs((prices[j][0] - prices[i][0]).days)
                if days_apart > 0:
                    change_per_day = abs(prices[i][1] - prices[j][1]) / days_apart
                    if change_per_day > threshold:
                        significant_changes.append((change_per_day, (prices[i], prices[j])))
        return significant_changes

# StockAnalyzer: Central class that integrates sorting, gain/loss, and anomaly detection
class StockAnalyzer:
    def __init__(self, file_paths):
        self.loader = DataLoader(file_paths)
        self.data = None

    def load_data(self):
        self.data = self.loader.load_data()
        return self.data

    def sort_data(self, key_column):
        sorter = MergeSort(key_column)
        sorted_data = sorter.sort(self.data)
        self._plot_sorted_data(sorted_data)
        return sorted_data

    def _plot_sorted_data(self, sorted_data):
        # Plot the sorted adjusted close prices
        plt.figure(figsize=(10, 6))
        plt.plot(sorted_data['Date'], sorted_data['Adjusted Close'], label='Sorted Adjusted Close Prices', color='blue')
        plt.title('Sorted Stock Prices Over Time')
        plt.xlabel('Date')
        plt.ylabel('Adjusted Close Price')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.legend()
        plt.show()

    def find_max_gain_loss_period(self):
        prices = self.data['Adjusted Close'].tolist()
        max_gain, start_idx, end_idx = MaxSubarray.find_max_gain(prices)
        self._plot_max_gain_loss_period(prices, start_idx, end_idx)
        return max_gain

    def _plot_max_gain_loss_period(self, prices, start_idx, end_idx):
        # Plot the maximum gain/loss period on the price graph
        plt.figure(figsize=(10, 6))
        dates = self.data['Date'].tolist()
        plt.plot(dates, prices, label='Adjusted Close Prices', color='blue')
        plt.axvspan(dates[start_idx], dates[end_idx], color='yellow', alpha=0.3, label='Max Gain/Loss Period')
        plt.title('Max Gain/Loss Period Highlighted')
        plt.xlabel('Date')
        plt.ylabel('Adjusted Close Price')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.legend()
        plt.show()

    def detect_anomalies(self, threshold):
        prices = self.data[['Date', 'Adjusted Close']].values.tolist()
        anomalies = SpikeDipClosestPair.find_all_significant_spikes_dips(prices, threshold)
        self._plot_anomalies(anomalies)
        return anomalies

    def _plot_anomalies(self, anomalies):
        # Plot the anomalies on the stock price graph
        plt.figure(figsize=(10, 6))
        dates = self.data['Date'].tolist()
        adj_close = self.data['Adjusted Close'].tolist()
        plt.plot(dates, adj_close, label='Adjusted Close Prices', color='blue')

        for change_per_day, (point1, point2) in anomalies:
            plt.scatter([point1[0], point2[0]], [point1[1], point2[1]], color='red', label=f'Anomaly {change_per_day:.2f}')

        plt.title('Anomalies in Stock Prices')
        plt.xlabel('Date')
        plt.ylabel('Adjusted Close Price')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.legend()
        plt.show()


# Main execution
analyzer = StockAnalyzer([r"C:\Storage\vscode\StockAnalyzer\data\A.csv"])
analyzer.load_data()

sorted_data = analyzer.sort_data("Date")
print(sorted_data.head(), '\n')

max_gain = analyzer.find_max_gain_loss_period()
print("Max gain/loss period:", max_gain, '\n')

anomalies = analyzer.detect_anomalies(threshold=10)
print("Anomalies detected:")

for anomaly in anomalies:
    print(anomaly)
