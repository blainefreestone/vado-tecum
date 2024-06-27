class Text:
    def __init__(self, title: str, author: str, content: list[list]) -> None:
        self.title = title
        self.author = author
        self.content = content
        
    def __str__(self):
        content = ["\n".join(chapter) for chapter in self.content]
        text = "\n\n".join(content)
        return f"{self.title}\n{self.author}\n\n{text}"
    
    @classmethod
    def from_string(cls, string: str) -> "Text":
        """
        Creates instance of Text from a string.
        The string should be formatted as follows:
        Title
        Author

        Chapter 1
        Text1

        Chapter 2
        Text2

        Args:
            string (str): The string to parse
        
        Returns:
            Text: A new instance of Text
        """
        # split the string into chapters and header (with title and author)
        lines = string.split("\n\n")

        # get the title and author from the header
        title, author = lines[0].split("\n")

        # get the content from the chapters
        content = [chapter.split("\n") for chapter in lines[1:]]

        # return a new Text object
        return cls(title, author, content)
    
    @classmethod
    def from_file(cls, filename: str) -> "Text":
        """
        Creates instance of Text from a file.
        The file should be formatted as follows:
        Title
        Author

        Chapter 1
        Text1

        Chapter 2
        Text2

        Args:
            filename (str): The filename to read from
        
        Returns:
            Text: A new instance of Text
        """
        with open(filename, "r") as file:
            return cls.from_string(file.read())

    def get_paragraph(self, paragraph: tuple) -> str | None:
        """
        Gets the paragraph at the given index.
        The paragraph index is a tuple with the chapter index and the paragraph index.

        Args:
            paragraph (tuple): The index of the paragraph to get
        
        Returns:
            str: The paragraph at the given index or None if the index is out of range
        """
        if paragraph[0] > len(self.content):
            return None
        chapter = self.content[paragraph[0] - 1]
        if paragraph[1] > len(chapter):
            return None
        return chapter[paragraph[1] - 1]

    def get_chapter(self, chapter: int) -> str | None:
        """
        Gets the chapter at the given index.
        The chapter index is an integer.

        Args:
            chapter (int): The index of the chapter to get

        Returns:
            str: The chapter at the given index or None if the index is out of range
        """
        if chapter > len(self.content):
            return None
        return "\n".join(self.content[chapter - 1])