from typing import List, Dict
from datetime import datetime

class ConversationState:
    def __init__(self, user: str):
        self.user = user
        self.messages: List[Dict[str, str]] = []
        self.context_stack: List[List[Dict[str, str]]] = [[]]  # Start with an empty root context
        self.start_time = datetime.now()
        self.last_update = self.start_time

    def add_message(self, role: str, content: str):
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.messages.append(message)
        self.context_stack[-1].append(message)  # Add to current context
        self.last_update = datetime.now()

    def push_context(self):
        """Start a new context."""
        self.context_stack.append([])

    def pop_context(self):
        """End the current context and return to the previous one."""
        if len(self.context_stack) > 1:
            return self.context_stack.pop()
        return None  # Can't pop the root context

    def get_current_context(self) -> List[Dict[str, str]]:
        """Get messages in the current context."""
        return self.context_stack[-1]

    def get_all_messages(self) -> List[Dict[str, str]]:
        """Get all messages across all contexts."""
        return self.messages

    def to_dict(self) -> Dict:
        return {
            "user": self.user,
            "messages": self.messages,
            "context_stack": self.context_stack,
            "start_time": self.start_time.isoformat(),
            "last_update": self.last_update.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict):
        conversation = cls(data["user"])
        conversation.messages = data["messages"]
        conversation.context_stack = data["context_stack"]
        conversation.start_time = datetime.fromisoformat(data["start_time"])
        conversation.last_update = datetime.fromisoformat(data["last_update"])
        return conversation