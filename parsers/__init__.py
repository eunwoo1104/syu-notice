from .academic import AcademicParser
from .aice import AICEParser
from .arch import ArchParser
from .base import BaseParser, Notice, RequestError, URLNotProvided
from .campus import CampusParser
from .cse import CSEParser
from .doba import DOBAParser
from .english import EnglishParser
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
    "english": EnglishParser,
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
