# Usage: Can be run from console with (e.g.)
# python -c "from CSV_Reader import DataSetReaderCsv; reader = DataSetReaderCsv(); dataset = reader.parse('csv1.csv'); print(f'Total: {dataset.sum()}, Average: {dataset.mean()}, Median: {dataset.median()}')"

"""
CSV Reader for processing numeric data files

Usage:
    from CSV_Reader import DataSetReaderCsv
    
    # Create a reader instance
    reader = DataSetReaderCsv()
    
    # Parse a CSV file and get a dataset
    dataset = reader.parse("path/to/your/file.csv")
    
    # Access statistical functions
    total = dataset.sum()
    avg = dataset.mean()
    middle = dataset.median()
    
Example commands:
    # Process sales data and get total sales
    python -c "from CSV_Reader import DataSetReaderCsv; reader = DataSetReaderCsv(); dataset = reader.parse('test1.csv'); print(f'Total sales: ${dataset.sum():,.2f}')"
    
    # Process quarterly sales and get average
    python -c "from CSV_Reader import DataSetReaderCsv; reader = DataSetReaderCsv(); dataset = reader.parse('test2.csv'); print(f'Average sale: ${dataset.mean():,.2f}')"
"""

import csv
from dataset import DataSet

class DataSetReaderCsv:
    """Reads numeric data from CSV files into DataSet objects"""
    
    def parse(self, filepath):
        """Parse CSV file and return a DataSet containing the numeric values.
        
        Args:
            filepath: Path to CSV file to parse
            
        Returns:
            DataSet: New dataset containing the numeric values
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file contains non-numeric values"""
        dataset = DataSet()
        
        try:
            with open(filepath, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    for value in row:
                        if value.strip():  # Skip empty values
                            try:
                                # Convert to float to handle both integers and decimals
                                num = float(value.strip())
                                dataset.include(num)
                            except ValueError:
                                # Skip non-numeric values silently
                                continue
                            
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find CSV file: {filepath}")
            
        return dataset

