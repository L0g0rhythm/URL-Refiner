import pytest
from url_refiner.core import process_urls, ProcessingMode, is_valid_url

# Test data for various scenarios
URLS_TO_TEST = [
    "https://example.com/page?user=admin&session=123",
    "http://test.com?id=abc&user=guest",
    "https://example.com/page?user=admin&session=123",  # Duplicate
    "http://test.com/other_path?id=abc&user=guest", # Same params, different path
    "invalid-url",
    ""
]

# 1. Tests for is_valid_url function
@pytest.mark.parametrize("url, expected", [
    ("http://example.com", True),
    ("https://example.com/path?q=1", True),
    ("ftp://user:pass@host:21/path", True),
    ("example.com", False),
    ("http//example.com", False),
    ("just a string", False),
    (None, False)
])
def test_is_valid_url(url, expected):
    """
    Tests the URL validation logic with various formats.
    """
    assert is_valid_url(url) == expected

# 2. Tests for process_urls function
def test_process_urls_in_replace_mode():
    """
    Tests if 'replace' mode correctly substitutes parameter values.
    """
    # Arrange
    config = {
        "mode": ProcessingMode.REPLACE.value,
        "value": "FUZZ",
        "exclude_params": [],
        "ignore_path": False
    }
    expected_data = [
        "https://example.com/page?user=FUZZ&session=FUZZ",
        "http://test.com?id=FUZZ&user=FUZZ",
        "http://test.com/other_path?id=FUZZ&user=FUZZ"
    ]
    expected_stats = {"total_input": 6, "total_output": 3, "duplicates_removed": 3}

    # Act
    result = process_urls(URLS_TO_TEST, config)

    # Assert
    assert result["data"] == expected_data
    assert result["stats"] == expected_stats

def test_process_urls_in_append_mode():
    """
    Tests if 'append' mode correctly appends values to parameters.
    """
    # Arrange
    config = {
        "mode": ProcessingMode.APPEND.value,
        "value": "_appended",
        "exclude_params": [],
        "ignore_path": False
    }
    expected_data = [
        "https://example.com/page?user=admin_appended&session=123_appended",
        "http://test.com?id=abc_appended&user=guest_appended",
        "http://test.com/other_path?id=abc_appended&user=guest_appended"
    ]
    
    # Act
    result = process_urls(URLS_TO_TEST, config)

    # Assert
    assert result["data"] == expected_data
    assert result["stats"]["total_output"] == 3

def test_process_urls_with_excluded_params():
    """
    Tests if the parameter exclusion functionality works correctly.
    """
    # Arrange
    config = {
        "mode": ProcessingMode.REPLACE.value,
        "value": "FUZZ",
        "exclude_params": ["session", "id"], # Exclude 'session' and 'id'
        "ignore_path": False
    }
    expected_data = [
        "https://example.com/page?user=FUZZ&session=123",
        "http://test.com?id=abc&user=FUZZ",
        "http://test.com/other_path?id=abc&user=FUZZ"
    ]
    
    # Act
    result = process_urls(URLS_TO_TEST, config)

    # Assert
    assert result["data"] == expected_data

def test_process_urls_with_ignore_path():
    """
    Tests if deduplication works correctly when ignoring the path.
    """
    # Arrange
    config = {
        "mode": ProcessingMode.REPLACE.value,
        "value": "FUZZ",
        "exclude_params": [],
        "ignore_path": True # Deduplicate based on domain and params only
    }
    # Expects the two 'test.com' URLs to be treated as duplicates
    expected_data = [
        "https://example.com/page?user=FUZZ&session=FUZZ",
        "http://test.com?id=FUZZ&user=FUZZ"
    ]
    expected_stats = {"total_input": 6, "total_output": 2, "duplicates_removed": 4}

    # Act
    result = process_urls(URLS_TO_TEST, config)

    # Assert
    assert result["data"] == expected_data
    assert result["stats"] == expected_stats

def test_process_urls_with_empty_input():
    """
    Tests if the function handles empty input gracefully.
    """
    # Arrange
    config = {"mode": ProcessingMode.REPLACE.value, "value": "FUZZ"}
    
    # Act
    result = process_urls([], config)
    
    # Assert
    assert result["data"] == []
    assert result["stats"] == {"total_input": 0, "total_output": 0, "duplicates_removed": 0}