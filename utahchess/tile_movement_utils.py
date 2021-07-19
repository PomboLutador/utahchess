from __future__ import annotations


def apply_movement_vector(
    position: tuple[int, int], movement_vector: tuple[int, int]
) -> tuple[int, int]:
    return position[0] + movement_vector[0], position[1] + movement_vector[1]


def is_in_bounds(position: tuple[int, int]) -> bool:
    return (0 <= position[0] <= 7) & (0 <= position[1] <= 7)
