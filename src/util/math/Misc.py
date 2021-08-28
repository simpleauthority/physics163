from math import floor, log


class MathHelpers:
    @staticmethod
    def extract_exponent_common(value):
        return MathHelpers.extract_exponent_base(10, value)

    @staticmethod
    def extract_exponent_base(base, value):
        return floor(log(abs(value), base))
