"""
This file is part of the Custom Gender Settings mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from cncustomgendersettings.dialogs.custom_gender_settings_dialog import CustomGenderSettingsDialog
from cncustomgendersettings.modinfo import ModInfo
from cncustomgendersettings.utils.cgs_setting_utils import CGSSettingUtils
from event_testing.results import TestResult
from interactions.context import InteractionContext
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.common_time_utils import CommonTimeUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

log = CommonLogRegistry.get().register_log(ModInfo.get_identity().name, 'custom_gender_settings_interaction')


class OpenCustomGenderSettingsInteraction(CommonImmediateSuperInteraction):
    """ Handle the interaction to open the Custom Gender Settings Dialog. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        log.debug('Running \'{}\' on_test.'.format(OpenCustomGenderSettingsInteraction.__name__))
        if interaction_target is None or not CommonTypeUtils.is_sim_instance(interaction_target):
            log.debug('Failed, Target is not a Sim.')
            return TestResult.NONE
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        if not CGSSettingUtils.is_enabled_for_custom_gender_setting_interactions(sim_info):
            log.debug('Failed, Active Sim is not enabled for CGS interactions.')
            return TestResult.NONE
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        if not CGSSettingUtils.is_enabled_for_custom_gender_setting_interactions(target_sim_info):
            log.debug('Failed, Target Sim is not enabled for CGS interactions.')
            return TestResult.NONE
        log.debug('Success.')
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        log.debug('Running \'{}\' on_started.'.format(OpenCustomGenderSettingsInteraction.__name__))
        if not CommonTypeUtils.is_sim_instance(interaction_target):
            log.debug('Target is not a sim.')
            return False
        CommonTimeUtils.pause_the_game()
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        CustomGenderSettingsDialog.open_custom_gender_settings(target_sim_info)
        return True
