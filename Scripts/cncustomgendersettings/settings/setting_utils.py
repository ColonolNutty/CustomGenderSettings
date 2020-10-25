"""
This file is part of the Custom Gender Settings mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any
from cncustomgendersettings.persistence.cgs_data_manager_utils import CGSDataManagerUtils
from cncustomgendersettings.settings.settings import CGSGlobalSetting
from sims.sim_info import SimInfo
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils


class CGSSettingUtils:
    """ Setting Utilities used by the CGS mod. """
    def __init__(self) -> None:
        self._data_manager = CGSDataManagerUtils()
        self.all_male_options = CGSSettingUtils.AllMaleOptions(self)
        self.all_female_options = CGSSettingUtils.AllFemaleOptions(self)

    def is_enabled_for_interactions(self, sim_info: SimInfo) -> bool:
        """ Determine if a Sim is enabled for Custom Gender Setting interactions. """
        return CommonAgeUtils.is_teen_adult_or_elder(sim_info)

    def force_all_sims_to_male(self) -> bool:
        """ Determine if all Sims should be forced to Male. """
        return self._is_forced_on(CGSGlobalSetting.ALL_SIMS_FORCE_AS_MALE)

    def force_all_sims_to_female(self) -> bool:
        """ Determine if all Sims should be forced to Male. """
        return self._is_forced_off(CGSGlobalSetting.ALL_SIMS_FORCE_AS_MALE)

    class AllMaleOptions:
        """ All Male Options. """
        def __init__(self, setting_utils: 'CGSSettingUtils'):
            self._setting_utils = setting_utils

        def force_breasts_on(self) -> bool:
            """ Determine if all Male Sims should have breasts. """
            return self._setting_utils._is_forced_on(CGSGlobalSetting.ALL_MALE_SIMS_BREASTS)

        def force_breasts_off(self) -> bool:
            """ Determine if all Male Sims should have no breasts. """
            return self._setting_utils._is_forced_off(CGSGlobalSetting.ALL_MALE_SIMS_BREASTS)

        def use_toilet_standing(self) -> bool:
            """ Determine if all Male Sims should use the toilet standing. """
            return self._setting_utils._is_forced_on(CGSGlobalSetting.ALL_MALE_SIMS_USE_TOILET_STANDING)

        def use_toilet_sitting(self) -> bool:
            """ Determine if all Male Sims should use the toilet sitting. """
            return self._setting_utils._is_forced_off(CGSGlobalSetting.ALL_MALE_SIMS_USE_TOILET_STANDING)

        def prefer_menswear(self) -> bool:
            """ Determine if all Male Sims should prefer menswear. """
            return self._setting_utils._is_forced_on(CGSGlobalSetting.ALL_MALE_SIMS_PREFER_MENSWEAR)

        def prefer_womenswear(self) -> bool:
            """ Determine if all Male Sims should prefer womenswear. """
            return self._setting_utils._is_forced_off(CGSGlobalSetting.ALL_MALE_SIMS_PREFER_MENSWEAR)

        def force_masculine_body_frame(self) -> bool:
            """ Determine if all Male Sims should use a masculine body frame. """
            return self._setting_utils._is_forced_on(CGSGlobalSetting.ALL_MALE_SIMS_HAVE_MASCULINE_FRAME)

        def force_feminine_body_frame(self) -> bool:
            """ Determine if all Male Sims should use a feminine body frame. """
            return self._setting_utils._is_forced_off(CGSGlobalSetting.ALL_MALE_SIMS_HAVE_MASCULINE_FRAME)

        def can_impregnate(self) -> bool:
            """ Determine if all Male Sims should be able to impregnate. """
            return self._setting_utils._is_forced_on(CGSGlobalSetting.ALL_MALE_SIMS_CAN_IMPREGNATE)

        def cannot_impregnate(self) -> bool:
            """ Determine if all Male Sims should not be able to impregnate. """
            return self._setting_utils._is_forced_off(CGSGlobalSetting.ALL_MALE_SIMS_CAN_IMPREGNATE)

        def can_be_impregnated(self) -> bool:
            """ Determine if all Male Sims should be able to be impregnated. """
            return self._setting_utils._is_forced_on(CGSGlobalSetting.ALL_MALE_SIMS_CAN_BE_IMPREGNATED)

        def cannot_be_impregnated(self) -> bool:
            """ Determine if all Male Sims should not be able to be impregnated. """
            return self._setting_utils._is_forced_off(CGSGlobalSetting.ALL_MALE_SIMS_CAN_BE_IMPREGNATED)

        def can_reproduce(self) -> bool:
            """ Determine if all Male Sims should be able to reproduce. """
            return self._setting_utils._is_forced_on(CGSGlobalSetting.ALL_MALE_SIMS_CAN_REPRODUCE)

        def cannot_reproduce(self) -> bool:
            """ Determine if all Male Sims should not be able to reproduce. """
            return self._setting_utils._is_forced_off(CGSGlobalSetting.ALL_MALE_SIMS_CAN_REPRODUCE)

    class AllFemaleOptions:
        """ All Female Options. """
        def __init__(self, setting_utils: 'CGSSettingUtils'):
            self._setting_utils = setting_utils

        def force_breasts_on(self) -> bool:
            """ Determine if all Female Sims should have breasts. """
            return self._setting_utils._is_forced_on(CGSGlobalSetting.ALL_FEMALE_SIMS_BREASTS)

        def force_breasts_off(self) -> bool:
            """ Determine if all Female Sims should have no breasts. """
            return self._setting_utils._is_forced_off(CGSGlobalSetting.ALL_FEMALE_SIMS_BREASTS)

        def use_toilet_standing(self) -> bool:
            """ Determine if all Female Sims should use the toilet standing. """
            return self._setting_utils._is_forced_on(CGSGlobalSetting.ALL_FEMALE_SIMS_USE_TOILET_STANDING)

        def use_toilet_sitting(self) -> bool:
            """ Determine if all Female Sims should use the toilet sitting. """
            return self._setting_utils._is_forced_off(CGSGlobalSetting.ALL_FEMALE_SIMS_USE_TOILET_STANDING)

        def prefer_menswear(self) -> bool:
            """ Determine if all Female Sims should prefer menswear. """
            return self._setting_utils._is_forced_on(CGSGlobalSetting.ALL_FEMALE_SIMS_PREFER_MENSWEAR)

        def prefer_womenswear(self) -> bool:
            """ Determine if all Female Sims should prefer womenswear. """
            return self._setting_utils._is_forced_off(CGSGlobalSetting.ALL_FEMALE_SIMS_PREFER_MENSWEAR)

        def force_masculine_body_frame(self) -> bool:
            """ Determine if all Female Sims should use a masculine body frame. """
            return self._setting_utils._is_forced_on(CGSGlobalSetting.ALL_FEMALE_SIMS_HAVE_MASCULINE_FRAME)

        def force_feminine_body_frame(self) -> bool:
            """ Determine if all Female Sims should use a feminine body frame. """
            return self._setting_utils._is_forced_off(CGSGlobalSetting.ALL_FEMALE_SIMS_HAVE_MASCULINE_FRAME)

        def can_impregnate(self) -> bool:
            """ Determine if all Female Sims should be able to impregnate. """
            return self._setting_utils._is_forced_on(CGSGlobalSetting.ALL_FEMALE_SIMS_CAN_IMPREGNATE)

        def cannot_impregnate(self) -> bool:
            """ Determine if all Female Sims should not be able to impregnate. """
            return self._setting_utils._is_forced_off(CGSGlobalSetting.ALL_FEMALE_SIMS_CAN_IMPREGNATE)

        def can_be_impregnated(self) -> bool:
            """ Determine if all Female Sims should be able to be impregnated. """
            return self._setting_utils._is_forced_on(CGSGlobalSetting.ALL_FEMALE_SIMS_CAN_BE_IMPREGNATED)

        def cannot_be_impregnated(self) -> bool:
            """ Determine if all Female Sims should not be able to be impregnated. """
            return self._setting_utils._is_forced_off(CGSGlobalSetting.ALL_FEMALE_SIMS_CAN_BE_IMPREGNATED)

        def can_reproduce(self) -> bool:
            """ Determine if all Female Sims should be able to reproduce. """
            return self._setting_utils._is_forced_on(CGSGlobalSetting.ALL_FEMALE_SIMS_CAN_REPRODUCE)

        def cannot_reproduce(self) -> bool:
            """ Determine if all Female Sims should not be able to reproduce. """
            return self._setting_utils._is_forced_off(CGSGlobalSetting.ALL_FEMALE_SIMS_CAN_REPRODUCE)

    def _is_forced_on(self, key: str) -> bool:
        return self._get_value(key) is True

    def _is_forced_off(self, key: str) -> bool:
        return self._get_value(key) is False

    def _is_disabled(self, key: str) -> bool:
        return self._get_value(key) is None

    def _get_value(self, key: str) -> Any:
        return self._data_manager.get_global_mod_settings_data_store().get_value_by_key(key)
