from .base import BaseParser, RequestError, URLNotProvided, Notice

from .academic import AcademicParser
from .aice import AICEParser
from .arch import ArchParser
from .campus import CampusParser
from .cse import CSEParser
from .doba import DOBAParser
from .event import EventParser
from .swuniv import SWUnivParser
from .teacher import TeacherParser

available_parsers: dict[str, type[BaseParser]] = {
    "academic": AcademicParser,
    "aice": AICEParser,
    "arch": ArchParser,
    "campus": CampusParser,
    "cse": CSEParser,
    "doba": DOBAParser,
    "event": EventParser,
    "swuniv": SWUnivParser,
    "teacher": TeacherParser,
}

__all__ = [
    "available_parsers",
    "BaseParser",
    "RequestError",
    "URLNotProvided",
    "Notice",
]
