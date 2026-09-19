from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Move:
    first: tuple[int, int]
    second: tuple[int, int]