def clamp(num: float, min_value: float, max_value: float):
    """
    Clamps a number between a minimum and maximum value.
    :param num: Number to clamp
    :param min_value: Minimum value
    :param max_value: Maximum value
    :return: Clamped number
    """
    return max(min(num, max_value), min_value)


def clamp_range(num: float, rng: tuple[float, float]):
    """
    Clamps a number between a minimum and maximum value.
    :param num: Number to clamp
    :param rng: Range to clamp to
    :return: Clamped number
    """
    return clamp(num, rng[0], rng[1])
