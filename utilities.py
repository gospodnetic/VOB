
def convert_to_percentage(fraction_array):
    return [element * 100 for element in fraction_array]

def set_precision(value, decimal_count):
    precision_value = 10 ** decimal_count
    return int(value * precision_value) / precision_value
