"""
Custom Gender Settings is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Dict
from customgendersettings.settings.settings import CGSGlobalSetting
from sims4communitylib.persistence.data_stores.common_data_store import CommonDataStore


class CGSGlobalSettingsDataStore(CommonDataStore):
    """ Manager of settings for CGS. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_identifier(cls) -> str:
        return 'cgs_global_settings'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def _version(self) -> int:
        return 1

    # noinspection PyMissingOrEmptyDocstring
    @property
    def _default_data(self) -> Dict[str, Any]:
        return {
            CGSGlobalSetting.VERSION: self._version,
            CGSGlobalSetting.ALL_SIMS_FORCE_AS_MALE: None,

            # Male Global Options
            CGSGlobalSetting.ALL_MALE_SIMS_BREASTS: None,
            CGSGlobalSetting.ALL_MALE_SIMS_USE_TOILET_STANDING: None,
            CGSGlobalSetting.ALL_MALE_SIMS_PREFER_MENSWEAR: None,
            CGSGlobalSetting.ALL_MALE_SIMS_HAVE_MASCULINE_FRAME: None,
            CGSGlobalSetting.ALL_MALE_SIMS_CAN_REPRODUCE: None,
            CGSGlobalSetting.ALL_MALE_SIMS_CAN_IMPREGNATE: None,
            CGSGlobalSetting.ALL_MALE_SIMS_CAN_BE_IMPREGNATED: None,
            CGSGlobalSetting.ALL_MALE_SIMS_REGENERATE_CLOTHING_ON_GENDER_OPTIONS_CHANGED: True,

            # Female Global Options
            CGSGlobalSetting.ALL_FEMALE_SIMS_BREASTS: None,
            CGSGlobalSetting.ALL_FEMALE_SIMS_USE_TOILET_STANDING: None,
            CGSGlobalSetting.ALL_FEMALE_SIMS_PREFER_MENSWEAR: None,
            CGSGlobalSetting.ALL_FEMALE_SIMS_HAVE_MASCULINE_FRAME: None,
            CGSGlobalSetting.ALL_FEMALE_SIMS_CAN_REPRODUCE: None,
            CGSGlobalSetting.ALL_FEMALE_SIMS_CAN_IMPREGNATE: None,
            CGSGlobalSetting.ALL_FEMALE_SIMS_CAN_BE_IMPREGNATED: None,
            CGSGlobalSetting.ALL_FEMALE_SIMS_REGENERATE_CLOTHING_ON_GENDER_OPTIONS_CHANGED: True,
        }.copy()
