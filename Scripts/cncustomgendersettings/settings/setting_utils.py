"""
This file is part of the Custom Gender Settings mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from cncustomgendersettings.enums.global_gender_options import CGSGender
from cncustomgendersettings.persistence.cgs_data_manager_utils import CGSDataManagerUtils
from cncustomgendersettings.settings.settings import CGSGlobalSetting
from sims.sim_info import SimInfo
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils


class CGSSettingUtils:
    """ Setting Utilities used by the CGS mod. """
    def __init__(self) -> None:
        self._data_manager = CGSDataManagerUtils()

    def is_enabled_for_interactions(self, sim_info: SimInfo) -> bool:
        """ Determine if a Sim is enabled for Custom Gender Setting interactions. """
        return CommonAgeUtils.is_teen_adult_or_elder(sim_info)

    def force_all_sims_to_male(self) -> bool:
        """ Determine if all Sims should be forced to Male. """
        return self._get_value(CGSGlobalSetting.FORCE_ALL_SIMS_TO_GENDER) == CGSGender.MALE

    def force_all_sims_to_female(self) -> bool:
        """ Determine if all Sims should be forced to Male. """
        return self._get_value(CGSGlobalSetting.FORCE_ALL_SIMS_TO_GENDER) == CGSGender.FEMALE

    def _get_value(self, key: str) -> Any:
        return self._data_manager.get_global_mod_settings_data_store().get_value_by_key(key)