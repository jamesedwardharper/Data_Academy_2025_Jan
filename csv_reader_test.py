import pytest
import os
import tempfile
from csv_reader import DataSetReaderCsv

@pytest.fixture
def reader():
    """Create a CSV reader instance"""
    return DataSetReaderCsv()

@pytest.fixture
def temp_dir():
    """Create and clean up a temporary directory"""
    dir_path = tempfile.mkdtemp()
    yield dir_path
    # Cleanup after test
    for file in os.listdir(dir_path):
        os.remove(os.path.join(dir_path, file))
    os.rmdir(dir_path)

def create_test_file(temp_dir, content):
    """Helper to create a temporary CSV file with given content"""
    fd, path = tempfile.mkstemp(suffix='.csv', dir=temp_dir)
    with os.fdopen(fd, 'w') as f:
        f.write(content)
    return path

def test_valid_numbers(reader, temp_dir):
    """Test parsing valid integer and decimal numbers"""
    csv_content = "1,2,3\n4.5,5.5,6.5"
    path = create_test_file(temp_dir, csv_content)
    dataset = reader.parse(path)
    assert dataset.sum() == pytest.approx(22.5)
    assert dataset.mean() == pytest.approx(3.75)

def test_mixed_content(reader, temp_dir):
    """Test handling mixed numeric and non-numeric content"""
    csv_content = "1,abc,2\n3,4.5,xyz"
    path = create_test_file(temp_dir, csv_content)
    dataset = reader.parse(path)
    assert dataset.sum() == pytest.approx(10.5)  # Should only sum the numbers
    assert dataset.mean() == pytest.approx(2.625)  # Average of 1,2,3,4.5

def test_empty_file(reader, temp_dir):
    """Test handling empty CSV file"""
    path = create_test_file(temp_dir, "")
    dataset = reader.parse(path)
    assert dataset.sum() == 0

def test_whitespace(reader, temp_dir):
    """Test handling whitespace in values"""
    csv_content = " 1 , 2 , 3 \n 4.5 , 5.5 , 6.5 "
    path = create_test_file(temp_dir, csv_content)
    dataset = reader.parse(path)
    assert dataset.sum() == pytest.approx(22.5)
    assert dataset.mean() == pytest.approx(3.75)

def test_empty_cells(reader, temp_dir):
    """Test handling empty cells in CSV"""
    csv_content = "1,,2\n,3,\n4,,"
    path = create_test_file(temp_dir, csv_content)
    dataset = reader.parse(path)
    assert dataset.sum() == pytest.approx(10.0)
    assert dataset.mean() == pytest.approx(2.5)  # Average of 1,2,3,4

def test_invalid_file(reader):
    """Test handling non-existent file"""
    with pytest.raises(FileNotFoundError):
        reader.parse("nonexistent.csv")

def test_scientific_notation(reader, temp_dir):
    """Test handling scientific notation"""
    csv_content = "1e2,2e-1,3E3"
    path = create_test_file(temp_dir, csv_content)
    dataset = reader.parse(path)
    assert dataset.sum() == pytest.approx(3100.2)
    assert dataset.mean() == pytest.approx(1033.4)  # Average of 100, 0.2, 3000
