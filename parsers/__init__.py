from .base import BaseParser, RequestError, URLNotProvided, Notice

from .academic import AcademicParser
from .cse import CSEParser
from .swuniv import SWUnivParser
from .teacher import TeacherParser

available_parsers: dict[str, type[BaseParser]] = {
    "academic": AcademicParser,
    "cse": CSEParser,
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
