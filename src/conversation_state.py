from typing import List, Dict
from datetime import datetime

class ConversationState:
    def __init__(self, user: str):
        self.user = user
        self.messages: List[Dict[str, str]] = []
        self.active_context: List[Dict[str, str]] = []
        self.start_time = datetime.now()
        self.last_update = self.start_time

    def add_message(self, role: str, content: str):
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        self.last_update = datetime.now()

    def get_messages(self) -> List[Dict[str, str]]:
        return self.messages

    def to_dict(self) -> Dict:
        return {
            "user": self.user,
            "messages": self.messages,
            "start_time": self.start_time.isoformat(),
            "last_update": self.last_update.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict):
        conversation = cls(data["user"])
        conversation.messages = data["messages"]
        conversation.active_context = data["active_context"]
        conversation.start_time = datetime.fromisoformat(data["start_time"])
        conversation.last_update = datetime.fromisoformat(data["last_update"])
        return conversation