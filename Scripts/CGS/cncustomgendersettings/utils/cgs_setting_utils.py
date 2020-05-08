"""
This file is part of the Custom Gender Settings mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils


class CGSSettingUtils:
    """ Setting Utilities used by the CGS mod. """
    def is_enabled_for_interactions(self, sim_info: SimInfo) -> bool:
        """ Determine if a Sim is enabled for Custom Gender Setting interactions. """
        return CommonAgeUtils.is_teen_adult_or_elder(sim_info)
