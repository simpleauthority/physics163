from math import floor, log10

from helper.Unit import Unit


class Convert:
    @staticmethod
    def scale_number(number, original_unit=Unit.BASE, desired_unit=Unit.BASE):
        """
        Scales a number to a specific power of 10 by first checking what its current power of 10 is then scaling
        appropriately. If original_unit is not specified, the function assumes the exponent on number implies the unit
        and will scale accordingly. If original_unit is specified, the original_unit's exponent will be
        taken into account before scaling occurs.
        """
        # Ensure original unit is not None
        if original_unit is None:
            original_unit = Unit.BASE

        # Combine number and original unit
        if original_unit is not Unit.BASE:
            number *= original_unit.value

        # Way ahead of you
        if desired_unit is Unit.BASE:
            return number

        # Get desired exponent
        desired_exp = floor(log10(abs(desired_unit.value)))

        # We are in base units. If desired exponent > 0 then we divide, as anything bigger will be fractional of our current value
        if desired_exp > 0:
            return number / desired_unit.value

        # Otherwise if desired exponent < 0 then we multiply, as anything smaller will be a multiple of our current value
        else:
            return number * (1 / desired_unit.value)

    @staticmethod
    def to_yotta(number, original_unit=Unit.BASE):
        """Helper function for bringing a number to Yotta (10^24)."""
        return Convert.scale_number(number, original_unit=original_unit, desired_unit=Unit.YOTTA)

    @staticmethod
    def to_zetta(number, original_unit=Unit.BASE):
        """Helper function for bringing a number to Zetta (10^21)."""
        return Convert.scale_number(number, original_unit=original_unit, desired_unit=Unit.ZETTA)

    @staticmethod
    def to_exa(number, original_unit=Unit.BASE):
        """Helper function for bringing a number to Exa (10^18)."""
        return Convert.scale_number(number, original_unit=original_unit, desired_unit=Unit.EXA)

    @staticmethod
    def to_peta(number, original_unit=Unit.BASE):
        """Helper function for bringing a number to Peta (10^15)"""
        return Convert.scale_number(number, original_unit=original_unit, desired_unit=Unit.PETA)

    @staticmethod
    def to_tera(number, original_unit=Unit.BASE):
        """Helper function for bringing a number to Tera (10^12)"""
        return Convert.scale_number(number, original_unit=original_unit, desired_unit=Unit.TERA)

    @staticmethod
    def to_giga(number, original_unit=Unit.BASE):
        """Helper function for bringing a number to Giga (10^9)"""
        return Convert.scale_number(number, original_unit=original_unit, desired_unit=Unit.GIGA)

    @staticmethod
    def to_mega(number, original_unit=Unit.BASE):
        """Helper function for bringing a number to Mega (10^6)"""
        return Convert.scale_number(number, original_unit=original_unit, desired_unit=Unit.MEGA)

    @staticmethod
    def to_kilo(number, original_unit=Unit.BASE):
        """Helper function for bringing a number to Kilo (10^3)"""
        return Convert.scale_number(number, original_unit=original_unit, desired_unit=Unit.KILO)

    @staticmethod
    def to_hecto(number, original_unit=Unit.BASE):
        """Helper function for bringing a number to Hecto (10^2)"""
        return Convert.scale_number(number, original_unit=original_unit, desired_unit=Unit.HECTO)

    @staticmethod
    def to_deka(number, original_unit=Unit.BASE):
        """Helper function for bringing a number to Deka (10^1)"""
        return Convert.scale_number(number, original_unit=original_unit, desired_unit=Unit.DEKA)

    @staticmethod
    def to_base(number, original_unit=Unit.BASE):
        """Helper function for bringing a number to Base SI (10^0)"""
        return Convert.scale_number(number, original_unit=original_unit, desired_unit=Unit.BASE)

    @staticmethod
    def to_deci(number, original_unit=Unit.BASE):
        """Helper function for bringing a number to Deci (10^-1)"""
        return Convert.scale_number(number, original_unit=original_unit, desired_unit=Unit.DECI)

    @staticmethod
    def to_centi(number, original_unit=Unit.BASE):
        """Helper function for bringing a number to Centi (10^-2)"""
        return Convert.scale_number(number, original_unit=original_unit, desired_unit=Unit.CENTI)

    @staticmethod
    def to_milli(number, original_unit=Unit.BASE):
        """Helper function for bringing a number to Milli (10^-3)"""
        return Convert.scale_number(number, original_unit=original_unit, desired_unit=Unit.MILLI)

    @staticmethod
    def to_micro(number, original_unit=Unit.BASE):
        """Helper function for bringing a number to Micro (10^-6)"""
        return Convert.scale_number(number, original_unit=original_unit, desired_unit=Unit.MICRO)

    @staticmethod
    def to_nano(number, original_unit=Unit.BASE):
        """Helper function for bringing a number to Nano (10^-9)"""
        return Convert.scale_number(number, original_unit=original_unit, desired_unit=Unit.NANO)

    @staticmethod
    def to_pico(number, original_unit=Unit.BASE):
        """Helper function for bringing a number to Pico (10^-12)"""
        return Convert.scale_number(number, original_unit=original_unit, desired_unit=Unit.PICO)

    @staticmethod
    def to_femto(number, original_unit=Unit.BASE):
        """Helper function for bringing a number to Femto (10^-15)"""
        return Convert.scale_number(number, original_unit=original_unit, desired_unit=Unit.FEMTO)

    @staticmethod
    def to_atto(number, original_unit=Unit.BASE):
        """Helper function for bringing a number to Atto (10^-18)"""
        return Convert.scale_number(number, original_unit=original_unit, desired_unit=Unit.ATTO)

    @staticmethod
    def to_zepto(number, original_unit=Unit.BASE):
        """Helper function for bringing a number to Zepto (10^-21)"""
        return Convert.scale_number(number, original_unit=original_unit, desired_unit=Unit.ZEPTO)

    @staticmethod
    def to_yocto(number, original_unit=Unit.BASE):
        """Helper function for bringing a number to Base SI (10^-24)"""
        return Convert.scale_number(number, original_unit=original_unit, desired_unit=Unit.YOCTO)
