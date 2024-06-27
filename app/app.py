import pickle
import pyinputplus as pyip
from app.user import User
from app.text import Text
import os
import yaml

class App:
    def __init__(self):
        self.users = []
        self.texts = []

    def add_user(self, user):
        self.users.append(user)

    def add_text(self, text):
        self.texts.append(text)

    def add_text_files(self, texts_path: str) -> None:
        """
        Add all the text files in the specified directory to the App object.

        Args:
            texts_path (str): The path to the directory containing the text files
        
        Returns:
            None
        """
        filenames = os.listdir(texts_path)
        for filename in filenames:
            file_path = os.path.join(texts_path, filename)
            text = Text.from_file(file_path)
            self.add_text(text)

    def save(self, file_path: str) -> None:
        """
        Save the App object to a file using pickle.

        Args:
            file_path (str): The path to the file to save the App object to
        
        Returns:
            None
        """
        with open(file_path, 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load(cls, file_path: str) -> str | None:
        """
        Loads an App object from a file using pickle.
        If the file does not exist, return None.

        Args:
            file_path (str): The path to the file to load the App object from
        
        Returns:
            App: The loaded App object
        """
        if not os.path.exists(file_path):
            return None

        with open(file_path, 'rb') as file:
            return pickle.load(file)

    def run(self):
        # choose the user
        name_to_user = {user.name: user for user in self.users}
        user_choice = pyip.inputMenu(list(name_to_user.keys()) + ['New User'], numbered=True, blank=True)
        
        if user_choice == 'New User':
            user_name = pyip.inputStr('Enter your name: ')
            user = User(user_name)
            self.add_user(user)
        else:
            user = name_to_user[user_choice]
        
        # choose the text
        title_to_text = {text.title: text for text in self.texts}
        text_choice = pyip.inputMenu(list(title_to_text.keys()) + ['New Text'], numbered=True, blank=True)
        
        if text_choice == 'New Text':
            new_text_choice = pyip.inputMenu(list(title_to_text.keys()), numbered=True, blank=True)
            selected_text = title_to_text[new_text_choice]
            user.assign_text(selected_text)
            text_choice = selected_text
        else:
            text_choice = title_to_text[text_choice]
        
        print(text_choice.content)
