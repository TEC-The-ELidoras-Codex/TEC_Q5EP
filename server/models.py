from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class GPS(BaseModel):
    lat: float
    lon: float
    accuracy: Optional[float] = None


class Device(BaseModel):
    user_agent: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    os: Optional[str] = None


class SubmissionMeta(BaseModel):
    id: str
    timestamp: str
    user_id: Optional[str] = None
    consent: bool = False
    tags: List[str] = Field(default_factory=list)
    gps: Optional[GPS] = None
    device: Optional[Device] = None
    context: Dict[str, Any] = Field(default_factory=dict)
    sha256_map: Dict[str, str] = Field(default_factory=dict)


class RunSummary(BaseModel):
    id: str
    timestamp: str
    tags: List[str] = Field(default_factory=list)
    has_photo: bool = False
    note_chars: int = 0


# Memory models
class MemoryItem(BaseModel):
    id: str
    timestamp: str
    user_id: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MemoryUpsert(BaseModel):
    user_id: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MemoryQuery(BaseModel):
    q: str
    tags: List[str] = Field(default_factory=list)
    limit: int = 10


class MemorySummary(BaseModel):
    id: str
    timestamp: str
    tags: List[str] = Field(default_factory=list)
    content_chars: int
