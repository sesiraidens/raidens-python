def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))

def lerp(start, end, t):
    return start + (end - start) * t

def deadband(value, threshold):
    if abs(value) < threshold:
        return 0
    return value

def ema(new_value, old_value, alpha=0.3):
    return alpha * new_value + (1 - alpha) * old_value