# Copyright (C) 2023 Callum Dickinson
#
# Buildarr is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# Buildarr is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with Buildarr.
# If not, see <https://www.gnu.org/licenses/>.


"""
Sonarr plugin type hints.
"""


from __future__ import annotations

import re

from pathlib import PurePosixPath, PureWindowsPath
from typing import Any, Callable, Generator, Literal

from pydantic import SecretStr
from typing_extensions import Self

SonarrProtocol = Literal["http", "https"]


class OSAgnosticPath(str):
    def is_windows(self) -> bool:
        return bool(re.match(r"^[A-Za-z]:", self) or self.startswith(r"\\"))

    def is_posix(self) -> bool:
        return not self.is_windows()

    def __add__(self, other: Any) -> OSAgnosticPath:
        return OSAgnosticPath(super().__add__(other))

    def __eq__(self, other: Any) -> bool:
        try:
            if self.is_windows():
                return PureWindowsPath(self) == PureWindowsPath(other)
            else:
                return PurePosixPath(self) == PurePosixPath(other)
        except TypeError:
            return False

    def __hash__(self) -> int:
        if self.is_windows():
            return hash(PureWindowsPath(self))
        else:
            return hash(PurePosixPath(self))

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[Any], Self], None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> Self:
        return cls(value)


class SonarrApiKey(SecretStr):
    """
    Constrained secret string type for a Sonarr API key.
    """

    min_length = 32
    max_length = 32
