"""
This file is part of the Custom Gender Settings mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Dict

from cncustomgendersettings.enums.global_gender_options import CGSGender
from cncustomgendersettings.settings.settings import CGSGlobalSetting
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
            CGSGlobalSetting.FORCE_ALL_SIMS_TO_GENDER: CGSGender.DISABLED
        }.copy()
