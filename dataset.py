import argparse
import requests
from bs4 import BeautifulSoup

class DataSet:
  def __init__(self):
    self._data = list()

  def include(self, data_point):
    if not isinstance(data_point, (int, float)):
      raise TypeError("Data point must be a number")
    self._data.append(data_point)

  def join(self, other_set):
    self._data += other_set._data

  def sum(self):
    """Returns the sum of all values in the dataset.
    If the dataset is empty, returns 0."""
    total = 0

    for data_point in self._data:
      total += data_point

    return total
  
  def mean(self):
    """Returns the arithmetic mean of all values in the dataset.
    If the dataset is empty, returns 0."""
    number_of_data_points = len(self._data)

    if number_of_data_points == 0:
      return 0
    
    return self.sum() / number_of_data_points
  
  def mode(self):
    """Returns the mode(s) of the dataset.
    If the dataset is empty, returns an empty list.
    If there are multiple modes, returns all of them in a list.
    Returns a single value if there is only one mode."""
    if len(self._data) == 0:
      return []
      
    # Count frequency of each value
    frequency = {}
    for value in self._data:
      frequency[value] = frequency.get(value, 0) + 1
    
    # Find the highest frequency
    max_frequency = max(frequency.values())
    
    # Get all values that appear max_frequency times
    modes = [value for value, count in frequency.items() 
            if count == max_frequency]
    
    # Return single value if only one mode or all values have same frequency
    # otherwise return list of modes
    if len(modes) == 1 or len(modes) == len(self._data):
        return sorted(modes)[0]
    return modes
  
  def median(self):
    """Returns the median value of the dataset.
    If the dataset is empty, returns 0.
    For even number of values, returns average of two middle values."""
    if len(self._data) == 0:
      return 0
      
    sorted_data = sorted(self._data)
    mid = len(sorted_data) // 2
    
    if len(sorted_data) % 2 == 0:
      # Even number of values - average the two middle values
      return (sorted_data[mid-1] + sorted_data[mid]) / 2
    else:
      # Odd number of values - return middle value
      return sorted_data[mid]
    
  def max(self):
    """Returns the maximum value in the dataset.
    If the dataset is empty, returns 0."""
    if len(self._data) == 0:
      return 0
    return max(self._data)
    
  def min(self):
    """Returns the minimum value in the dataset.
    If the dataset is empty, returns 0."""
    if len(self._data) == 0:
      return 0
    return min(self._data)
    
  def range(self):
    """Returns a tuple of (min, max) values in the dataset.
    If the dataset is empty, returns (0, 0)."""
    if len(self._data) == 0:
      return (0, 0)
    return (min(self._data), max(self._data))
    
  def window(self, lower_bound, upper_bound):
    """Returns count of values that lie within the bounds (inclusive).
    Args:
        lower_bound: Lower boundary of the window
        upper_bound: Upper boundary of the window
    Returns:
        int: Number of values within the window bounds"""
    return sum(1 for x in self._data if lower_bound <= x <= upper_bound)
    


def main():
    parser = argparse.ArgumentParser(description='Read numeric data from URL into a DataSet')
    parser.add_argument('--url', help='URL to scrape for numbers', required=True)
    args = parser.parse_args()
    
    try:
        reader = DataSetReaderWeb()
        dataset = reader.parse(args.url)
            
        print(f"Successfully loaded {len(dataset._data)} values")
        print(f"Sum: {dataset.sum()}")
        print(f"Mean: {dataset.mean()}")
        print(f"Median: {dataset.median()}")
        print(f"Mode: {dataset.mode()}")
        print(f"Range: {dataset.range()}")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {str(e)}")
        exit(1)

class DataSetReaderWeb:
    """Reads numeric data from web pages into DataSet objects"""
    
    def parse(self, url):
        """Parse webpage and return a DataSet containing any numeric values found.
        
        Args:
            url: URL of webpage to parse
            
        Returns:
            DataSet: New dataset containing the numeric values
            
        Raises:
            ValueError: If URL is invalid or connection fails
            ValueError: If no numeric values are found
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all text nodes
            texts = soup.stripped_strings
            
            dataset = DataSet()
            for text in texts:
                # Try to convert any numeric strings to float
                try:
                    num = float(text.strip())
                    dataset.include(num)
                except ValueError:
                    continue
                    
            if len(dataset._data) == 0:
                raise ValueError(f"No numeric values found at URL: {url}")
                
            return dataset
            
        except requests.RequestException as e:
            raise ValueError(f"Failed to fetch URL {url}: {str(e)}")

if __name__ == "__main__":
    main()
