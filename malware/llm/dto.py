from dataclasses import dataclass

from serde import serde


@serde
@dataclass
class FileMetadata:
    path: str
    name: str
    extension: str
    size_kb: int
    last_modified: str
    preview: str


@serde
@dataclass
class BackupCandidate:
    path: str
    reason: str
    risk_level: str
