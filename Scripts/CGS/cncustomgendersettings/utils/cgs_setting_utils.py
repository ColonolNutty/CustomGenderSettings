"""
This file is part of the Custom Gender Settings mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.utils.sims.common_age_species_utils import CommonAgeSpeciesUtils


class CGSSettingUtils:
    """ Setting Utilities used by the CGS mod. """
    @staticmethod
    def is_enabled_for_custom_gender_setting_interactions(sim_info: SimInfo) -> bool:
        """ Determine if a Sim is enabled for Custom Gender Setting interactions. """
        return CommonAgeSpeciesUtils.is_teen_adult_or_elder_human(sim_info)
