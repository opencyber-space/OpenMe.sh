from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from enum import Enum


@dataclass
class SessionMessage:
    session_id: str = ''
    subject_id: str = ''
    message_data: Dict[str, Any] = field(default_factory=dict)
    message_data_template: Dict[str, Any] = field(default_factory=dict)
    reception_channel_id: str = ''
    expiry_date: int = 0
    status: str = 'pending'
    dsl_execution_id: str = ''

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SessionMessage':
        return cls(
            session_id=data.get('session_id', ''),
            subject_id=data.get('subject_id', ''),
            message_data=data.get('message_data', {}),
            message_data_template=data.get('message_data_template', {}),
            reception_channel_id=data.get('reception_channel_id', ''),
            expiry_date=data.get('expiry_date', 0),
            status=data.get('status', 'pending'),
            dsl_execution_id=data.get('dsl_execution_id', '')
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'session_id': self.session_id,
            'subject_id': self.subject_id,
            'message_data': self.message_data,
            'message_data_template': self.message_data_template,
            'reception_channel_id': self.reception_channel_id,
            'expiry_date': self.expiry_date,
            'status': self.status,
            'dsl_execution_id': self.dsl_execution_id
        }


@dataclass
class ValidationResult:
    is_valid: bool
    errors: Optional[Dict[str, Any]] = field(default_factory=dict)
    warnings: Optional[Dict[str, Any]] = field(default_factory=dict)
    validated_at: Optional[int] = None


class SessionStatus(Enum):
    PENDING = "pending"
    VALIDATED = "validated"
    EXPIRED = "expired"
    FAILED = "failed"
    COMPLETED = "completed"