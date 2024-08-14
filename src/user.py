from src.text import Text
from src.user_text import UserText

class User:
    """
    Class to represent a unique user using the application.
    Meant to be used to store user information to personalize the application.
    """
    def __init__(self, name):
        self.name = name
        self.texts = []

    def __str__(self):
        return f'User: {self.name}'
    
    def assign_text(self, text: Text) -> None:
        """
        Assigns a text to the user.
        The text is represented as a UserText object.
        
        Args:
            text (Text): The text to assign to the user
        
        Returns:
            None
        """
        user_text = UserText(text, self)
        self.texts.append(user_text)