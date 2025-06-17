from dataclasses import dataclass, field, asdict
from typing import Dict, Any
import uuid
import time


@dataclass
class ChatSession:
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = ''
    subject_id: str = ''
    org_id: str = ''
    session_metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChatSession':
        return cls(
            session_id=data.get('session_id', str(uuid.uuid4())),
            user_id=data.get('user_id', ''),
            subject_id=data.get('subject_id', ''),
            org_id=data.get('org_id', ''),
            session_metadata=data.get('session_metadata', {})
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ChatMessage:
    chat_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str = ''
    message_json: Dict[str, Any] = field(default_factory=dict)
    file_urls: Dict[str, str] = field(default_factory=dict)
    type: str = ''  # 'user' or 'system'
    timestamp: int = field(default_factory=lambda: int(time.time()))

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChatMessage':
        return cls(
            chat_id=data.get('chat_id', str(uuid.uuid4())),
            session_id=data.get('session_id', ''),
            message_json=data.get('message_json', {}),
            file_urls=data.get('file_urls', {}),
            type=data.get('type', ''),
            timestamp=data.get('timestamp', int(time.time()))
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
