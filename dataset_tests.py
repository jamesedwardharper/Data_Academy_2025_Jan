import pytest
import os
from dataset import DataSet, DataSetReaderWeb

# Tests for DataSet constructor

def test_new_dataset_is_empty():
    # Arrange
    dataset = DataSet()
    
    # Assert
    assert len(dataset._data) == 0

# Tests for DataSet: Include function

def test_include_adds_single_value():
    # Arrange
    dataset = DataSet()
    
    # Act
    dataset.include(5)
    
    # Assert
    assert dataset._data == [5]

def test_include_adds_negative_value():
    # Arrange
    dataset = DataSet()
    
    # Act
    dataset.include(-5)
    
    # Assert
    assert dataset._data == [-5]

def test_include_invalid_type():
    # Arrange
    dataset = DataSet()
    
    # Act & Assert
    with pytest.raises(TypeError):
        dataset.include("not a number")

# Tests for DataSet: Join function

def test_join_two_datasets():
    # Arrange
    dataset1 = DataSet()
    dataset1.include(1)
    dataset1.include(2)
    
    dataset2 = DataSet()
    dataset2.include(3)
    dataset2.include(4)
    
    # Act
    dataset1.join(dataset2)
    
    # Assert
    assert dataset1._data == [1, 2, 3, 4]

# Tests for DataSet: Sum function

def test_sum_with_negative_values():
    # Arrange
    dataset = DataSet()
    dataset.include(-1)
    dataset.include(-2)
    dataset.include(-3)
    
    # Act
    result = dataset.sum()
    
    # Assert
    assert result == -6

def test_sum_with_mixed_values():
    # Arrange
    dataset = DataSet()
    dataset.include(-1)
    dataset.include(0)
    dataset.include(1)
    
    # Act
    result = dataset.sum()
    
    # Assert
    assert result == 0

def test_sum_with_multiple_values():
    # Arrange
    dataset = DataSet()
    dataset.include(1)
    dataset.include(2)
    dataset.include(3)
    
    # Act
    result = dataset.sum()
    
    # Assert
    assert result == 6

def test_sum_empty_dataset():
    # Arrange
    dataset = DataSet()
    
    # Act
    result = dataset.sum()
    
    # Assert
    assert result == 0

# Tests for DataSet: Mean function

def test_mean_with_negative_values():
    # Arrange
    dataset = DataSet()
    dataset.include(-2)
    dataset.include(-4)
    dataset.include(-6)
    
    # Act
    result = dataset.mean()
    
    # Assert
    assert result == -4

def test_mean_with_mixed_values():
    # Arrange
    dataset = DataSet()
    dataset.include(-1)
    dataset.include(0)
    dataset.include(1)
    
    # Act
    result = dataset.mean()
    
    # Assert
    assert result == 0

def test_mean_with_values():
    # Arrange
    dataset = DataSet()
    dataset.include(2)
    dataset.include(4)
    dataset.include(6)
    
    # Act
    result = dataset.mean()
    
    # Assert
    assert result == 4

def test_mean_empty_dataset():
    # Arrange
    dataset = DataSet()
    
    # Act
    result = dataset.mean()
    
    # Assert
    assert result == 0

# Tests for DataSet: Mode function

def test_mode_with_negative_values():
    # Arrange
    dataset = DataSet()
    dataset.include(-1)
    dataset.include(-2)
    dataset.include(-2)
    dataset.include(-3)
    
    # Act
    result = dataset.mode()
    
    # Assert
    assert result == -2

def test_mode_with_mixed_values():
    # Arrange
    dataset = DataSet()
    dataset.include(-1)
    dataset.include(-1)
    dataset.include(0)
    dataset.include(1)
    
    # Act
    result = dataset.mode()
    
    # Assert
    assert result == -1

def test_mode_single_mode():
    # Arrange
    dataset = DataSet()
    dataset.include(1)
    dataset.include(2)
    dataset.include(2)
    dataset.include(3)
    
    # Act
    result = dataset.mode()
    
    # Assert
    assert result == 2

def test_mode_multiple_modes():
    # Arrange
    dataset = DataSet()
    dataset.include(1)
    dataset.include(1)
    dataset.include(2)
    dataset.include(2)
    dataset.include(3)
    
    # Act
    result = dataset.mode()
    
    # Assert
    assert sorted(result) == [1, 2]

def test_mode_empty_dataset():
    # Arrange
    dataset = DataSet()
    
    # Act
    result = dataset.mode()
    
    # Assert
    assert result == []

def test_mode_all_unique_values():
    # Arrange
    dataset = DataSet()
    dataset.include(1)
    dataset.include(2)
    dataset.include(3)
    
    # Act
    result = dataset.mode()
    
    # Assert
    assert result == 1  # Returns smallest value when all frequencies are equal

# Tests for DataSet: Median function

def test_median_odd_number_of_values():
    # Arrange
    dataset = DataSet()
    dataset.include(1)
    dataset.include(3)
    dataset.include(2)
    
    # Act
    result = dataset.median()
    
    # Assert
    assert result == 2

def test_median_even_number_of_values():
    # Arrange
    dataset = DataSet()
    dataset.include(1)
    dataset.include(2)
    dataset.include(3)
    dataset.include(4)
    
    # Act
    result = dataset.median()
    
    # Assert
    assert result == 2.5

def test_median_empty_dataset():
    # Arrange
    dataset = DataSet()
    
    # Act
    result = dataset.median()
    
    # Assert
    assert result == 0

def test_median_unsorted_values():
    # Arrange
    dataset = DataSet()
    dataset.include(5)
    dataset.include(2)
    dataset.include(1)
    dataset.include(4)
    dataset.include(3)
    
    # Act
    result = dataset.median()
    
    # Assert
    assert result == 3

# Tests for DataSet: Max function

def test_max_with_positive_values():
    # Arrange
    dataset = DataSet()
    dataset.include(2)
    dataset.include(4)
    dataset.include(6)
    
    # Act
    result = dataset.mean()
    
    # Assert
    assert result == 4

def test_max_with_negative_values():
    # Arrange
    dataset = DataSet()
    dataset.include(-1)
    dataset.include(-5)
    dataset.include(-3)
    
    # Act
    result = dataset.max()
    
    # Assert
    assert result == -1

def test_max_empty_dataset():
    # Arrange
    dataset = DataSet()
    
    # Act
    result = dataset.max()
    
    # Assert
    assert result == 0

# Tests for DataSet: Min function

def test_min_with_positive_values():
    # Arrange
    dataset = DataSet()
    dataset.include(1)
    dataset.include(5)
    dataset.include(3)
    
    # Act
    result = dataset.min()
    
    # Assert
    assert result == 1

def test_min_with_negative_values():
    # Arrange
    dataset = DataSet()
    dataset.include(-1)
    dataset.include(-5)
    dataset.include(-3)
    
    # Act
    result = dataset.min()
    
    # Assert
    assert result == -5

def test_min_empty_dataset():
    # Arrange
    dataset = DataSet()
    
    # Act
    result = dataset.min()
    
    # Assert
    assert result == 0


# Tests for DataSet: Range function

def test_range_with_positive_values():
    # Arrange
    dataset = DataSet()
    dataset.include(1)
    dataset.include(2)
    dataset.include(3)
    
    # Act
    result = dataset.window(0, 5)
    
    # Assert
    assert result == 3

def test_range_with_negative_values():
    # Arrange
    dataset = DataSet()
    dataset.include(-1)
    dataset.include(-5)
    dataset.include(-3)
    
    # Act
    result = dataset.range()
    
    # Assert
    assert result == (-5, -1)

def test_range_empty_dataset():
    # Arrange
    dataset = DataSet()
    
    # Act
    result = dataset.range()
    
    # Assert
    assert result == (0, 0)


# Tests for DataSet: Window function

def test_window_with_negative_bounds():
    # Arrange
    dataset = DataSet()
    dataset.include(-5)
    dataset.include(-3)
    dataset.include(-1)
    dataset.include(0)
    
    # Act
    result = dataset.window(-4, -2)
    
    # Assert
    assert result == 1

def test_window_invalid_bounds():
    # Arrange
    dataset = DataSet()
    dataset.include(1)
    dataset.include(2)
    
    # Act & Assert
    with pytest.raises(TypeError):
        dataset.window("invalid", 5)
    with pytest.raises(TypeError):
        dataset.window(1, "invalid")

def test_window_reversed_bounds():
    # Arrange
    dataset = DataSet()
    dataset.include(1)
    dataset.include(2)
    dataset.include(3)
    
    # Act
    result = dataset.window(5, 2)  # Upper bound < Lower bound
    
    # Assert
    assert result == 0

def test_window_some_values_in_range():
    # Arrange
    dataset = DataSet()
    dataset.include(1)
    dataset.include(5)
    dataset.include(3)
    dataset.include(10)
    
    # Act
    result = dataset.window(2, 6)
    
    # Assert
    assert result == 2

def test_window_no_values_in_range():
    # Arrange
    dataset = DataSet()
    dataset.include(1)
    dataset.include(2)
    dataset.include(3)
    
    # Act
    result = dataset.window(10, 20)
    
    # Assert
    assert result == 0

def test_window_empty_dataset():
    # Arrange
    dataset = DataSet()
    
    # Act
    result = dataset.window(0, 10)
    
    # Assert
    assert result == 0

# Tests for DataSetReaderWeb: Parse function

def test_web_reader_parses_numbers():
    # Arrange
    reader = DataSetReaderWeb()
    url = "https://cyan-ali-20.tiiny.site/"
    
    # Act
    dataset = reader.parse(url)
    
    # Assert
    assert len(dataset._data) == 4  # Should find 4 numeric values
    assert 6 in dataset._data  # Alan's score
    assert 18 in dataset._data  # Dan's score
    assert 17 in dataset._data  # Rosie's score
    assert 4 in dataset._data  # Ellen's score
    assert dataset.sum() == 45  # Total of all scores

def test_web_reader_invalid_url():
    # Arrange
    reader = DataSetReaderWeb()
    
    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        reader.parse("https://invalid.url.that.does.not.exist")
    assert "Failed to fetch URL" in str(exc_info.value)

def test_web_reader_no_numbers():
    # Arrange
    reader = DataSetReaderWeb()
    
    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        reader.parse("https://example.com")
    assert "No numeric values found" in str(exc_info.value)
