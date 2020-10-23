"""
This file is part of the Custom Gender Settings mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CGSGender(CommonInt):
    """ Gender """
    DISABLED = -1
    MALE = 0
    FEMALE = 1


class CGSToiletUsage(CommonInt):
    """ Toilet usage. """
    DISABLED = -1
    TOILET_STANDING = 0
    TOILET_SITTING = 1


class CGSClothingPreference(CommonInt):
    """ Clothing Preference """
    DISABLED = -1
    MENSWEAR = 0
    WOMANSWEAR = 1


class CGSFrame(CommonInt):
    """ Can Impregnate """
    DISABLED = -1
    MASCULINE = 0
    FEMININE = 1


class CGSCanImpregnate(CommonInt):
    """ Can Impregnate """
    DISABLED = -1
    CAN_IMPREGNATE = 0
    CANNOT_IMPREGNATE = 1


class CGSCanBeImpregnated(CommonInt):
    """ Can Be Impregnated """
    DISABLED = -1
    CAN_BE_IMPREGNATED = 0
    CANNOT_BE_IMPREGNATED = 1


class CGSCanReproduce(CommonInt):
    """ Can Reproduce """
    DISABLED = -1
    CAN_REPRODUCE = 0
    CANNOT_REPRODUCE = 1
