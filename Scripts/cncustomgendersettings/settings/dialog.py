"""
This file is part of the Custom Gender Settings mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable

from cncustomgendersettings.enums.global_gender_options import CGSGender
from cncustomgendersettings.enums.strings_enum import CGSStringId
from cncustomgendersettings.global_gender_options_injection import _CGSUpdateGenderOptions
from cncustomgendersettings.modinfo import ModInfo
from cncustomgendersettings.persistence.cgs_data_manager_utils import CGSDataManagerUtils
from cncustomgendersettings.settings.settings import CGSGlobalSetting
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_action_option import \
    CommonDialogActionOption
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_select_option import \
    CommonDialogSelectOption
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CGSGlobalSettingsDialog(HasLog):
    """ Settings. """
    def __init__(self, sim_info: SimInfo, on_close: Callable[[], Any]=None):
        super().__init__()
        self._sim_info = sim_info
        self._on_close = on_close
        self._data_store = CGSDataManagerUtils().get_global_mod_settings_data_store()
        self._restart_required = False

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cgs_settings'

    def open(self) -> None:
        """ Open Dialog. """
        def _on_close() -> None:
            if self._on_close is not None:
                self._on_close()

        def _reopen() -> None:
            self.open()

        option_dialog = CommonChooseObjectOptionDialog(
            CGSStringId.GLOBAL_SETTINGS_NAME,
            CGSStringId.GLOBAL_SETTINGS_DESCRIPTION,
            mod_identity=self.mod_identity,
            on_close=_on_close
        )

        @CommonExceptionHandler.catch_exceptions(self.mod_identity)
        def _on_force_all_chosen(_: str, picked_option: int):
            if picked_option is None:
                return
            self._data_store.set_value_by_key(_, picked_option)
            if picked_option == CGSGender.DISABLED:
                _reopen()
                return

            for sim_info in CommonSimUtils.get_instanced_sim_info_for_all_sims_generator():
                _CGSUpdateGenderOptions()._update_gender_options(sim_info)
            _reopen()

        current_force_all_val = self._data_store.get_value_by_key(CGSGlobalSetting.FORCE_ALL_SIMS_TO_GENDER)
        force_all_selected_string = CGSStringId.DISABLED
        if current_force_all_val == CGSGender.MALE:
            force_all_selected_string = CGSStringId.MALE
        elif current_force_all_val == CGSGender.FEMALE:
            force_all_selected_string = CGSStringId.FEMALE

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    CGSStringId.FORCE_ALL_SIMS_TO_GENDER_NAME,
                    CGSStringId.FORCE_ALL_SIMS_TO_GENDER_DESCRIPTION,
                    title_tokens=(force_all_selected_string,)
                ),
                on_chosen=lambda *_, **__: self._select_option(
                    CGSStringId.FORCE_ALL_SIMS_TO_GENDER_NAME,
                    CGSStringId.FORCE_ALL_SIMS_TO_GENDER_DESCRIPTION,
                    force_all_selected_string,
                    CGSGlobalSetting.FORCE_ALL_SIMS_TO_GENDER,
                    CGSStringId.MALE,
                    CGSStringId.FEMALE,
                    CGSGender.MALE,
                    CGSGender.FEMALE,
                    CGSGender.DISABLED,
                    on_chosen=_on_force_all_chosen,
                    on_close=_reopen
                )
            )
        )

        option_dialog.show()

    def _select_option(self, title: int, description: LocalizedString, current_string: int, setting_name: str, on_name: int, off_name: int, on: Any, off: Any, disabled: Any, on_chosen: Callable[[str, int], Any], on_close: Callable[[], Any]=None):
        def _on_close() -> None:
            if on_close is not None:
                on_close()

        option_dialog = CommonChooseObjectOptionDialog(
            title,
            description,
            title_tokens=(current_string, ),
            mod_identity=self.mod_identity,
            on_close=_on_close
        )

        current_val = self._data_store.get_value_by_key(setting_name)

        @CommonExceptionHandler.catch_exceptions(self.mod_identity)
        def _on_chosen(_: str, picked_option: int):
            if picked_option is None:
                _on_close()
                return
            on_chosen(_, picked_option)

        option_dialog.add_option(
            CommonDialogSelectOption(
                setting_name,
                disabled,
                CommonDialogOptionContext(
                    CGSStringId.DISABLED,
                    0,
                    icon=CommonIconUtils.load_filled_circle_icon() if current_val == disabled else CommonIconUtils.load_unfilled_circle_icon()
                ),
                on_chosen=_on_chosen
            )
        )

        option_dialog.add_option(
            CommonDialogSelectOption(
                setting_name,
                on,
                CommonDialogOptionContext(
                    on_name,
                    0,
                    icon=CommonIconUtils.load_filled_circle_icon() if current_val == on else CommonIconUtils.load_unfilled_circle_icon()
                ),
                on_chosen=_on_chosen
            )
        )

        option_dialog.add_option(
            CommonDialogSelectOption(
                setting_name,
                off,
                CommonDialogOptionContext(
                    off_name,
                    0,
                    icon=CommonIconUtils.load_filled_circle_icon() if current_val == off else CommonIconUtils.load_unfilled_circle_icon()
                ),
                on_chosen=_on_chosen
            )
        )

        option_dialog.show()
