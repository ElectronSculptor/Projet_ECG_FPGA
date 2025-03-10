"""
This module is responsible for implementing the class used to check object types.
It's implemented by the professor, Raphael VIERA.
"""

import serial



class CheckIf:
    """
    This class implements the methods responsible for checking object types
    """
    def __init__(self):
        pass

    @staticmethod
    def is_list(element):
        """
        Check if element is of type list.

        Args:
            - element: list

        Returns:
            - : bool
        """

        return isinstance(element, list)

    @staticmethod
    def is_set(element):
        """
        Check if element is of type set.

        Args:
            - element: set

        Returns:
            - : bool
        """

        return isinstance(element, set)

    @staticmethod
    def is_tuple(element):
        """
        Check if element is of type tuple.

        Args:
            - element: tuple

        Returns:
            - : bool
        """

        return isinstance(element, tuple)

    @staticmethod
    def is_string(element):
        """
        Check if element is of type string.

        Args:
            - element: str

        Returns:
            - : bool
        """

        return isinstance(element, str)

    @staticmethod
    def is_bool(element):
        """
        Check if element is of type bool.

        Args:
            - element: bool

        Returns:
            - : bool
        """

        try:
            if isinstance(element, bool):
                return True
            else:
                return False
        except:
            return False

    @staticmethod
    def is_in_range(val, range):
        """
        Check if val is in range.

        Args:
            - val: float
            - range: list

        Returns:
            - : bool
        """

        try:
            if min(range) <= val <= max(range):
                return True
            else:
                return False
        except:
            return False

    @staticmethod
    def is_hashable_type(obj):
        """
        Check if element is hashable.

        Args:
            - element: obj

        Returns:
            - : bool
        """

        import collections
        return isinstance(obj, collections.abc.Hashable)

    @staticmethod
    def is_value_in_enum(user_param_enum, user_param_value):
        try:
            get_verification_parameter = getattr(user_param_enum, user_param_value)
            temp = get_verification_parameter.value

            return True
        except:
            # exiting here because the parameter does not exist in the ENUM
            return False

    @staticmethod
    def is_number(to_check):
        """
        Check if element is of type number even if it's a string that can be converted to a number.

        Args:
            - to_check: str or int or float or bool

        Returns:
            - : bool
        """

        # int(False) = 0 but it is not a number.
        # 0 == False so checking if to_check is
        try:
            if isinstance(to_check, bool):
                return False
        except:
            pass

        try:
            float(to_check)
            return True
        except:  # ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(to_check)
            return True
        except:  # (TypeError, ValueError):
            pass

        return False
