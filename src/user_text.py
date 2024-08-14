class UserText:
    def __init__(self, text, user):
        self.text = text
        self.user = user
        self.location = (1, 1)

    def update_location(self, chapter: int, paragraph: int) -> None:
        """
        Updates the location of the UserText object.
        The location is represented as a tuple (chapter, paragraph).

        Args:
            chapter (int): The chapter to move to
            paragraph (int): The paragraph to move to
        
        Returns:
            None
        """
        if chapter > len(self.text.content):
            chapter = len(self.text.content)
            paragraph = len(self.text.content[-1])
        
        self.location = (chapter, paragraph)