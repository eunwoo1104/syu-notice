from .base import BaseParser, RequestError, URLNotProvided, Notice

from .academic import AcademicParser
from .aice import AICEParser
from .arch import ArchParser
from .cse import CSEParser
from .doba import DOBAParser
from .swuniv import SWUnivParser
from .teacher import TeacherParser

available_parsers: dict[str, type[BaseParser]] = {
    "academic": AcademicParser,
    "aice": AICEParser,
    "arch": ArchParser,
    "cse": CSEParser,
    "doba": DOBAParser,
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
