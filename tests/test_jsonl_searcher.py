import pytest
import os
import json
import pickle
from app.jsonl_searcher import JSONLIndexer, JSONLSearcher

@pytest.fixture
def temp_jsonl_file(tmp_path):
    file_path = tmp_path / "test.jsonl"
    data = [
        {"word": "apple", "definition": "A fruit"},
        {"word": "banana", "definition": "Another fruit"},
        {"word": "cherry", "definition": "Yet another fruit"},
        {"word": "apple", "definition": "A tech company"}
    ]
    with open(file_path, 'w', encoding='utf-8') as f:
        for entry in data:
            f.write(json.dumps(entry) + "\n")
    return file_path

def test_create_index(temp_jsonl_file):
    indexer = JSONLIndexer(temp_jsonl_file)
    indexer.create_index()
    
    assert os.path.exists(indexer.index_path), "Index file should be created"

    with open(indexer.index_path, 'rb') as f:
        index = pickle.load(f)
    
    assert "apple" in index, "Index should contain 'apple'"
    assert "banana" in index, "Index should contain 'banana'"
    assert "cherry" in index, "Index should contain 'cherry'"

def test_load_index(temp_jsonl_file):
    indexer = JSONLIndexer(temp_jsonl_file)
    indexer.create_index()
    index = indexer.load_index()
    
    assert "apple" in index, "Index should contain 'apple'"
    assert "banana" in index, "Index should contain 'banana'"
    assert "cherry" in index, "Index should contain 'cherry'"

def test_search(temp_jsonl_file):
    searcher = JSONLSearcher(temp_jsonl_file)
    
    result = searcher.search("apple")
    assert isinstance(result, list), "Search should return a list"
    assert len(result) == 2, "Search should return two results for 'apple'"
    assert result[0]["word"] == "apple", "First result should contain the word 'apple'"
    assert result[0]["definition"] == "A fruit", "First result should contain the correct definition for 'apple'"
    assert result[1]["word"] == "apple", "Second result should contain the word 'apple'"
    assert result[1]["definition"] == "A tech company", "Second result should contain the correct definition for 'apple'"
    
    result = searcher.search("banana")
    assert isinstance(result, list), "Search should return a list"
    assert len(result) == 1, "Search should return one result for 'banana'"
    assert result[0]["word"] == "banana", "Result should contain the word 'banana'"
    assert result[0]["definition"] == "Another fruit", "Result should contain the correct definition for 'banana'"
    
    result = searcher.search("cherry")
    assert isinstance(result, list), "Search should return a list"
    assert len(result) == 1, "Search should return one result for 'cherry'"
    assert result[0]["word"] == "cherry", "Result should contain the word 'cherry'"
    assert result[0]["definition"] == "Yet another fruit", "Result should contain the correct definition for 'cherry'"
    
    result = searcher.search("durian")
    assert result == [], "Search should return an empty list for a word not in the index"