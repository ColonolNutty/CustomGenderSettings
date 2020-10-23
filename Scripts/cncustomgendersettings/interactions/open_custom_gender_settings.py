"""
This file is part of the Custom Gender Settings mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from cncustomgendersettings.dialogs.custom_gender_settings_dialog import CustomGenderSettingsDialog
from cncustomgendersettings.modinfo import ModInfo
from cncustomgendersettings.settings.setting_utils import CGSSettingUtils
from event_testing.results import TestResult
from interactions.context import InteractionContext
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_time_utils import CommonTimeUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class OpenCustomGenderSettingsInteraction(CommonImmediateSuperInteraction):
    """ Handle the interaction to open the Custom Gender Settings Dialog. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cgs_open_settings'

    @classmethod
    def _get_setting_utils(cls) -> CGSSettingUtils:
        return CGSSettingUtils()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        cls.get_log().debug('Running \'{}\' on_test.'.format(OpenCustomGenderSettingsInteraction.__name__))
        if interaction_target is None or not CommonTypeUtils.is_sim_instance(interaction_target):
            cls.get_log().debug('Failed, Target is not a Sim.')
            return TestResult.NONE
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        if not cls._get_setting_utils().is_enabled_for_interactions(sim_info):
            cls.get_log().debug('Failed, Active Sim is not enabled for CGS interactions.')
            return TestResult.NONE
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        if not cls._get_setting_utils().is_enabled_for_interactions(target_sim_info):
            cls.get_log().debug('Failed, Target Sim is not enabled for CGS interactions.')
            return TestResult.NONE
        cls.get_log().debug('Success, can open Custom Gender Settings.')
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        self.log.debug('Running \'{}\' on_started.'.format(OpenCustomGenderSettingsInteraction.__name__))
        if not CommonTypeUtils.is_sim_instance(interaction_target):
            self.log.debug('Target is not a sim.')
            return False
        CommonTimeUtils.pause_the_game()
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        CustomGenderSettingsDialog().open(target_sim_info)
        return True
