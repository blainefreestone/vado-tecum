import pytest
import os
import json
import pickle
from app.jsonl_searcher import JSONLIndexer, JSONLSearcher

'''
TODO: Randomly select 10 or so words from the JSONL file and write tests to check if the search method returns the correct results for those words.
TODO: Decide exactly how I want the search result to be formatted. Should it retain its format or should I extract the data and create a new structure?
'''

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

def test_get_word_info():
    searcher = JSONLSearcher('tests/word_objects.jsonl')
    
    result = searcher.get_word_info("inpleremus")
    assert len(result) == 1, "Search result should have 1 entry"
    assert result[0]["word"] == "inpleremus", "Search result should have the word 'inpleremus'"
    assert result[0]["pos"] == "verb", "Search result should have the pos 'verb'"
    assert result[0]["glosses"] == ["first-person plural imperfect active subjunctive of inpleō"], "Search result should have the gloss 'first-person plural imperfect active subjunctive of inpleō'"
    assert result[0]["form_of_words"] == ["inpleō"], "Search result should have the form of word 'inpleō'"

    result = searcher.get_word_info("circumnavigaratis")
    assert len(result) == 1, "Search result should have 1 entry"
    assert result[0]["word"] == "circumnavigaratis", "Search result should have the word 'circumnavigaratis'"
    assert result[0]["pos"] == "verb", "Search result should have the pos 'verb'"
    assert result[0]["glosses"] == ["second-person plural pluperfect active indicative of circumnāvigō"], "Search result should have the gloss 'second-person plural pluperfect active indicative of circumnāvigō'"
    assert result[0]["form_of_words"] == ["circumnāvigō"], "Search result should have the form of word 'circumnāvigō'"

    result = searcher.get_word_info("providentius")
    assert len(result) == 1, "Search result should have 1 entry"
    assert result[0]["word"] == "providentius", "Search result should have the word 'providentius'"
    assert result[0]["pos"] == "adv", "Search result should have the pos 'adv'"
    assert result[0]["glosses"] == ["comparative degree of prōvidenter"], "Search result should have the gloss 'comparative degree of prōvidenter'"
    assert result[0]["form_of_words"] == ["prōvidenter"], "Search result should have the form of word 'prōvidenter'"

    result = searcher.get_word_info("clarissime")
    assert len(result) == 1, "Search result should have 1 entry"
    assert result[0]["word"] == "clarissime", "Search result should have the word 'clarissime'"
    assert result[0]["pos"] == "adv", "Search result should have the pos 'adv'"
    assert result[0]["glosses"] == ["superlative degree of clārē: most clearly"], "Search result should have the gloss 'superlative degree of clārē: most clearly'"
    assert result[0]["form_of_words"] == ["clārē"], "Search result should have the form of word 'clārē'"

    result = searcher.get_word_info("multiflorus")
    assert len(result) == 1, "Search result should have 1 entry"
    assert result[0]["word"] == "multiflorus", "Search result should have the word 'multiflorus'"
    assert result[0]["pos"] == "adj", "Search result should have the pos 'adj'"
    assert result[0]["glosses"] == ["having many-flowers"], "Search result should have the gloss 'having many-flowers'"
    assert result[0]["form_of_words"] == [], "Search result should have an empty list for form_of_words"

    result = searcher.get_word_info("tranquillus")
    assert len(result) == 1, "Search result should have 1 entry"
    assert result[0]["word"] == "tranquillus", "Search result should have the word 'tranquillus'"
    assert result[0]["pos"] == "adj", "Search result should have the pos 'adj'"
    assert result[0]["glosses"] == ["quiet, calm, still, tranquil", "placid, composed, untroubled, undisturbed"], "Search result should have the glosses 'quiet, calm, still, tranquil' and 'placid, composed, untroubled, undisturbed'"
    assert result[0]["form_of_words"] == [], "Search result should not have 'form_of_words'"