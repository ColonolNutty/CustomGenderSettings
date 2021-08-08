"""
This file is part of the Custom Gender Settings mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
# noinspection PyBroadException
try:
    from customgendersettings.dialogs.custom_gender_settings_dialog import CustomGenderSettingsDialog
    from customgendersettings.enums.strings_enum import CGSStringId
    from customgendersettings.interactions.open_custom_gender_settings import OpenCustomGenderSettingsInteraction
    from customgendersettings.modinfo import ModInfo
    from customgendersettings.settings.setting_utils import CGSSettingUtils
    from sims4communitylib.enums.strings_enum import CommonStringId
    from typing import Callable, Any, Union
    from sims.sim_info import SimInfo
    from sims4communitylib.mod_support.mod_identity import CommonModIdentity
    from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
    from sims4communitylib.utils.common_type_utils import CommonTypeUtils
    from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
    from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
    from sims4modsettingsmenu.registration.mod_settings_menu_item import S4MSMMenuItem
    from sims4modsettingsmenu.registration.mod_settings_registry import S4MSMModSettingsRegistry
    from event_testing.results import TestResult
    from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
    from sims4communitylib.utils.common_log_registry import CommonLogRegistry
    from protocolbuffers.Localization_pb2 import LocalizedString


    class _CGSMSMMenuItem(S4MSMMenuItem):
        # noinspection PyMissingOrEmptyDocstring
        @property
        def mod_identity(self) -> CommonModIdentity:
            return ModInfo.get_identity()

        # noinspection PyMissingOrEmptyDocstring
        @property
        def title(self) -> CommonStringId:
            return CommonStringId.CUSTOM_GENDER_SETTINGS

        # noinspection PyMissingOrEmptyDocstring
        @property
        def description(self) -> Union[int, str, LocalizedString, None]:
            return CGSStringId.CGS_CUSTOM_GENDER_SETTINGS_DESCRIPTION

        # noinspection PyMissingOrEmptyDocstring
        @property
        def log_identifier(self) -> str:
            return 'cgs_msm_menu_item'

        # noinspection PyMissingOrEmptyDocstring
        def is_available_for(self, source_sim_info: SimInfo, target: Any=None) -> bool:
            self.log.debug('Checking if {} is available for \'{}\' and Target \'{}\'.'.format(self.mod_identity.name, CommonSimNameUtils.get_full_name(source_sim_info), target))
            if target is None or not CommonTypeUtils.is_sim_or_sim_info(target):
                self.log.debug('Failed, Target is not a Sim.')
                return False
            if not CGSSettingUtils().is_enabled_for_interactions(source_sim_info):
                self.log.debug('Failed, Source Sim is not enabled for interactions.')
                return TestResult.NONE
            target_sim_info = CommonSimUtils.get_sim_info(target)
            if not CGSSettingUtils().is_enabled_for_interactions(target_sim_info):
                self.log.debug('Failed, Target Sim is not enabled for interactions.')
                return False
            self.log.debug('Menu is available for Source Sim and Target Sim.')
            return True

        # noinspection PyMissingOrEmptyDocstring
        def show(
            self,
            source_sim_info: SimInfo,
            *args,
            target: Any=None,
            on_close: Callable[..., Any]=CommonFunctionUtils.noop,
            **kwargs
        ):
            self.log.format_with_message('Showing Dialog.', mod_name=self.mod_identity.name)
            target_sim_info = CommonSimUtils.get_sim_info(target)
            CustomGenderSettingsDialog(target_sim_info, on_close=on_close).open()


    S4MSMModSettingsRegistry().register_menu_item(_CGSMSMMenuItem())

    log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'cgs_settings')

    # noinspection PyUnusedLocal
    @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), OpenCustomGenderSettingsInteraction, OpenCustomGenderSettingsInteraction.on_test.__name__)
    def _cgs_hide_normal_settings_interaction(original, cls, *_, **__) -> TestResult:
        log.debug('Hiding the CGS Open Dialog interaction in favor of the Mod Settings Menu.')
        return TestResult.NONE
except:
    pass
