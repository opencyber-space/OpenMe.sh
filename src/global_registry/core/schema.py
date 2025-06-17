from dataclasses import dataclass, field, asdict
from typing import Dict, Any
import uuid


@dataclass
class BackboneDataObject:
    system_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    org_ids: str = ''
    cluster_id: str = ''
    public_url: str = ''
    metadata: Dict[str, Any] = field(default_factory=dict)
    name: str = ''

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BackboneDataObject':
        return cls(
            system_id=str(data.get('system_id', uuid.uuid4())),
            org_ids=data.get('org_ids', ''),
            cluster_id=data.get('cluster_id', ''),
            public_url=data.get('public_url', ''),
            metadata=data.get('metadata', {}),
            name=data.get('name', '')
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
