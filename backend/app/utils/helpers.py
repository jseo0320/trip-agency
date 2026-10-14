def clamp(value: float, minimum: float = 0, maximum: float = 100) -> float:
    return min(maximum,max(minimum,value))
