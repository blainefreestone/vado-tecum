import json
import mmap
import os
import pickle
from typing import Dict, Any, List

class JSONLIndexer:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.index_path = f"{file_path}.index"

    def create_index(self):
        index = {}
        with open(self.file_path, 'rb') as f:
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            position = 0
            for line in iter(mm.readline, b''):
                data = json.loads(line)
                word = data.get('word')
                if word:
                    if word not in index:
                        index[word] = []
                    index[word].append(position)
                position = mm.tell()
                
        with open(self.index_path, 'wb') as f:
            pickle.dump(index, f)

    def load_index(self) -> Dict[str, List[int]]:
        with open(self.index_path, 'rb') as f:
            return pickle.load(f)

class JSONLSearcher:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.indexer = JSONLIndexer(file_path)
        if not os.path.exists(self.indexer.index_path):
            print("Creating index...")
            self.indexer.create_index()
        self.index = self.indexer.load_index()

    def get_word_info(self, word: str) -> List[Dict[str, Any]]:
        positions = self.index.get(word)
        if positions is None:
            return []
        
        results = []
        with open(self.file_path, 'rb') as file:
            mm = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
            for position in positions:
                mm.seek(position)
                line = mm.readline()
                loaded_line = json.loads(line)
                results.append(loaded_line)

        word_info_list = []

        # extract word information
        for result in results:
            # extract basic information
            result_word = result.get('word', 'Unknown')
            result_pos = result.get('pos', 'Unknown')
            
            # extract glosses and form of words from the senses
            senses = result.get('senses', [])
            glosses = []
            form_of_words = []
            for sense in senses:
                glosses.extend(sense.get('glosses', []))
                form_of_words.extend([form.get('word') for form in sense.get('form_of', [])])

            word_info_list.append({
                "word": result_word,
                "pos": result_pos,
                "glosses": glosses,
                "form_of_words": form_of_words
            })
        
        return word_info_list