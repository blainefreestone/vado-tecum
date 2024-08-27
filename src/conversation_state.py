from user import User
from typing import List, Dict, Tuple
from datetime import datetime

class ConversationState:
    def __init__(self, user: User):
        self.user: User = user
        self.messages: List[Dict[str, str]] = []
        self.context_stack: List[Tuple[int, int]] = [(0, 0)]  # (start_index, end_index)
        self.start_time = datetime.now()
        self.last_update = self.start_time

    def add_message(self, role: str, content: str):
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.messages.append(message)
        start, end = self.context_stack[-1]
        self.context_stack[-1] = (start, end + 1)
        self.last_update = datetime.now()

    def push_context(self):
        """Start a new context."""
        current_end = self.context_stack[-1][1]
        self.context_stack.append((current_end, current_end))

    def pop_context(self):
        """End the current context and return to the previous one."""
        if len(self.context_stack) > 1:
            return self.context_stack.pop()
        return None  # Can't pop the root context

    def get_current_context(self) -> List[Dict[str, str]]:
        """Get messages in the current context and all parent contexts."""
        return self.messages[:self.context_stack[-1][1]]

    def get_context_messages(self, context_index: int) -> List[Dict[str, str]]:
        """Get messages for a specific context."""
        if 0 <= context_index < len(self.context_stack):
            start, end = self.context_stack[context_index]
            return self.messages[start:end]
        return []

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