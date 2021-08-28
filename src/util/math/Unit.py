from enum import Enum

from util.math.Misc import Misc


class Unit(Enum):
    """
    Defines SI prefixes and their related exponents
    """
    YOTTA = 1e24
    ZETTA = 1e21
    EXA = 1e18
    PETA = 1e15
    TERA = 1e12
    GIGA = 1e9
    MEGA = 1e6
    KILO = 1e3
    HECTO = 1e2
    DEKA = 1e1
    BASE = 1e0  # convenience
    DECI = 1e-1
    CENTI = 1e-2
    MILLI = 1e-3
    MICRO = 1e-6
    NANO = 1e-9
    PICO = 1e-12
    FEMTO = 1e-15
    ATTO = 1e-18
    ZEPTO = 1e-21
    YOCTO = 1e-24

    @staticmethod
    def determine_unit(value):
        """Determines the unit of a number by extracting its exponent and then comparing the exponents"""
        print("INFO: Determining unit for {0}...".format(value))

        value_exp = Misc.extract_exponent_common(value)

        for item in Unit:
            item_exp = Misc.extract_exponent_common(item.value)

            if value_exp == item_exp:
                print("INFO: Unit for {0} is {1}".format(value, item))

                return item
