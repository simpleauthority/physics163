from math import floor, log


class Misc:
    @staticmethod
    def extract_exponent_common(value):
        return Misc.extract_exponent_base(10, value)

    @staticmethod
    def extract_exponent_base(base, value):
        return floor(log(abs(value), base))
