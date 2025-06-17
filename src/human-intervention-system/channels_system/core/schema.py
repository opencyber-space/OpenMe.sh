from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class ChannelStoreObject:
    channel_id: str = ''
    channel_name: str = ''
    channel_description: str = ''
    channel_metadata: Dict[str, Any] = field(default_factory=dict)
    channel_tags: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChannelStoreObject':
        return cls(
            channel_id=data.get('channel_id', ''),
            channel_name=data.get('channel_name', ''),
            channel_description=data.get('channel_description', ''),
            channel_metadata=data.get('channel_metadata', {}),
            channel_tags=data.get('channel_tags', [])
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'channel_id': self.channel_id,
            'channel_name': self.channel_name,
            'channel_description': self.channel_description,
            'channel_metadata': self.channel_metadata,
            'channel_tags': self.channel_tags
        }
