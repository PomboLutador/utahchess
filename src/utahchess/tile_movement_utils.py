from __future__ import annotations


def apply_movement_vector(
    position: tuple[int, int], movement_vector: tuple[int, int]
) -> tuple[int, int]:
    """Get a tile with a movement vector applied.

    Does not check whether the resulting tile is out of bounds or not.
    """
    return position[0] + movement_vector[0], position[1] + movement_vector[1]


def apply_movement_vector_n_times(
    position: tuple[int, int],
    movement_vector: tuple[int, int],
    n: int,
) -> tuple[int, int]:
    """Get a tile with a movement vector applied n times.

    Does not check whether the resulting tile is out of bounds or not.
    """
    position_to_return = position
    while n > 0:
        position_to_return = (
            position_to_return[0] + movement_vector[0],
            position_to_return[1] + movement_vector[1],
        )
        n -= 1
    return position_to_return


def is_in_bounds(position: tuple[int, int]) -> bool:
    return (0 <= position[0] <= 7) & (0 <= position[1] <= 7)
