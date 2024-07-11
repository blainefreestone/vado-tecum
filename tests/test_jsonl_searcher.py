import pytest
import os
import json
import pickle
from app.jsonl_searcher import JSONLIndexer, JSONLSearcher

@pytest.fixture
def temp_jsonl_file(tmp_path):
    file_path = tmp_path / "test.jsonl"
    data = [
        {"pos": "verb", "head_templates": [{"name": "head", "args": {"1": "la", "2": "verb form", "head": "abacināte"}, "expansion": "abacināte"}], "forms": [{"form": "abacināte", "tags": ["canonical"]}], "word": "abacinate", "lang": "Latin", "lang_code": "la", "senses": [{"links": [["abacinō", "abacino#Latin"]], "glosses": ["second-person plural present active imperative of abacinō"], "tags": ["active", "form-of", "imperative", "plural", "present", "second-person"], "form_of": [{"word": "abacinō"}], "id": "en-abacinate-la-verb-V2vYEsGz", "categories": [{"name": "Latin entries with incorrect language header", "kind": "other", "parents": ["Entries with incorrect language header", "Entry maintenance"], "source": "w"}]}]},
        {"pos": "adv", "head_templates": [{"name": "la-adv", "args": {"1": "abdicātīvē", "2": "-"}, "expansion": "abdicātīvē (not comparable)"}], "forms": [{"form": "abdicātīvē", "tags": ["canonical"]}], "sounds": [{"ipa": "/ab.di.kaːˈtiː.u̯eː/", "tags": ["Classical-Latin"]}, {"ipa": "[äbd̪ɪkäːˈt̪iːu̯eː]", "tags": ["Classical-Latin"]}, {"ipa": "/ab.di.kaˈti.ve/", "note": "modern Italianate Ecclesiastical"}, {"ipa": "[äbd̪ikäˈt̪iːve]", "note": "modern Italianate Ecclesiastical"}], "etymology_number": 1, "etymology_text": "From abdicatīvus (“negative”) + -ē.", "etymology_templates": [{"name": "affix", "args": {"1": "la", "2": "abdicatīvus", "3": "-ē", "gloss1": "negative"}, "expansion": "abdicatīvus (“negative”) + -ē"}], "word": "abdicative", "lang": "Latin", "lang_code": "la", "senses": [{"links": [["negatively", "negatively"]], "glosses": ["negatively"], "tags": ["not-comparable"], "id": "en-abdicative-la-adv-RuK4EQPZ", "categories": [{"name": "Latin terms suffixed with -e", "kind": "other", "parents": [], "source": "w+disamb"}]}]},
        {"pos": "verb", "head_templates": [{"name": "head", "args": {"1": "la", "2": "verb form", "head": "abnōdāte"}, "expansion": "abnōdāte"}], "forms": [{"form": "abnōdāte", "tags": ["canonical"]}], "word": "abnodate", "lang": "Latin", "lang_code": "la", "senses": [{"links": [["abnōdō", "abnodo#Latin"]], "glosses": ["second-person plural present active imperative of abnōdō"], "tags": ["active", "form-of", "imperative", "plural", "present", "second-person"], "form_of": [{"word": "abnōdō"}], "id": "en-abnodate-la-verb-2c6GyDfc", "categories": [{"name": "Latin entries with incorrect language header", "kind": "other", "parents": ["Entries with incorrect language header", "Entry maintenance"], "source": "w"}]}]}
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
    
    assert "abacinate" in index, "Index should contain 'abacinate'"
    assert "abdicative" in index, "Index should contain 'abdicative'"
    assert "abnodate" in index, "Index should contain 'abnodate'"

def test_load_index(temp_jsonl_file):
    indexer = JSONLIndexer(temp_jsonl_file)
    indexer.create_index()
    index = indexer.load_index()
    
    assert "abacinate" in index, "Index should contain 'abacinate'"
    assert "abdicative" in index, "Index should contain 'abdicative'"
    assert "abnodate" in index, "Index should contain 'abnodate'"

def test_search(temp_jsonl_file):
    searcher = JSONLSearcher(temp_jsonl_file)
    
    result = searcher.search("abacinate")
    assert isinstance(result, list), "Search should return a list"
    assert len(result) == 1, "Search should return two results for 'abacinate'"
    assert result[0]["word"] == "abacinate", "First result should contain the word 'abacinate'"
    assert result[0]["senses"][0]["glosses"] == ["second-person plural present active imperative of abacinō"], "First result should contain the correct senses for 'abacinate'"

    result = searcher.search("abdicative")
    assert isinstance(result, list), "Search should return a list"
    assert len(result) == 1, "Search should return one result for 'abdicative'"
    assert result[0]["word"] == "abdicative", "Result should contain the word 'abdicative'"
    assert result[0]["senses"][0]["glosses"] == ["negatively"], "Result should contain the correct senses for 'abdicative'"
    
    result = searcher.search("abnodate")
    assert isinstance(result, list), "Search should return a list"
    assert len(result) == 1, "Search should return one result for 'abnodate'"
    assert result[0]["word"] == "abnodate", "Result should contain the word 'abnodate'"
    assert result[0]["senses"][0]["glosses"] == ["second-person plural present active imperative of abnōdō"], "Result should contain the correct senses for 'abnodate'"
    
    result = searcher.search("amo")
    assert result == [], "Search should return an empty list for a word not in the index"