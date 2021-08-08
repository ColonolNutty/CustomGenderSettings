"""
Custom Gender Settings is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable, Union
from customgendersettings.enums.strings_enum import CGSStringId
from customgendersettings.global_gender_options_injection import _CGSUpdateGenderOptions
from customgendersettings.logging.has_cgs_log import HasCGSLog
from customgendersettings.modinfo import ModInfo
from customgendersettings.persistence.cgs_data_manager_utils import CGSDataManagerUtils
from customgendersettings.settings.settings import CGSGlobalSetting
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.ok_cancel_dialog import CommonOkCancelDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_action_option import \
    CommonDialogActionOption
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_select_option import \
    CommonDialogSelectOption
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CGSGlobalSettingsDialog(HasCGSLog):
    """ Settings. """
    def __init__(self, sim_info: SimInfo, on_close: Callable[[], Any]=None):
        super().__init__()
        self._sim_info = sim_info
        self._on_close = on_close
        self._data_store = CGSDataManagerUtils().get_global_mod_settings_data_store()

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

        def _reopen(*_, **__) -> None:
            self.open()

        option_dialog = CommonChooseObjectOptionDialog(
            CGSStringId.GLOBAL_SETTINGS_NAME,
            CGSStringId.GLOBAL_SETTINGS_DESCRIPTION,
            mod_identity=self.mod_identity,
            on_close=_on_close
        )

        @CommonExceptionHandler.catch_exceptions(self.mod_identity)
        def _on_force_all_chosen(_: str, picked_option: Union[int, bool]):
            if picked_option is None:
                return
            if picked_option == -1:
                self._data_store.set_value_by_key(_, None)
                _reopen()
                return

            @CommonExceptionHandler.catch_exceptions(self.mod_identity)
            def _on_ok(_d) -> None:
                self.log.debug('Ok chosen {}, \'{}\''.format(picked_option, _))
                self._data_store.set_value_by_key(_, picked_option)
                self.log.format_with_message('set value with', val=self._data_store.get_value_by_key(_))

                for sim_info in CommonSimUtils.get_instanced_sim_info_for_all_sims_generator():
                    _CGSUpdateGenderOptions()._update_gender_options(sim_info)
                _reopen()

            def _on_cancel(_d) -> None:
                self.log.debug('Cancel chosen')
                _reopen()

            CommonOkCancelDialog(
                CGSStringId.PLEASE_CONFIRM_NAME,
                CGSStringId.PLEASE_CONFIRM_DESCRIPTION,
                ok_text_identifier=CGSStringId.YES_UPDATE_ALL_SIMS,
                cancel_text_identifier=CGSStringId.NO
            ).show(
                on_ok_selected=_on_ok,
                on_cancel_selected=_on_cancel
            )

        current_force_all_val = self._data_store.get_value_by_key(CGSGlobalSetting.ALL_SIMS_FORCE_AS_MALE)
        force_all_selected_string = CGSStringId.DISABLED
        if current_force_all_val is True:
            force_all_selected_string = CGSStringId.MALE
        elif current_force_all_val is False:
            force_all_selected_string = CGSStringId.FEMALE

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    CGSStringId.CGS_FORCE_ALL_SIMS_TO_GENDER_NAME,
                    CGSStringId.CGS_FORCE_ALL_SIMS_TO_GENDER_DESCRIPTION,
                    title_tokens=(force_all_selected_string,)
                ),
                on_chosen=lambda *_, **__: self._select_option(
                    CGSStringId.CGS_FORCE_ALL_SIMS_TO_GENDER_NAME,
                    CGSStringId.CGS_FORCE_ALL_SIMS_TO_GENDER_DESCRIPTION,
                    force_all_selected_string,
                    CGSGlobalSetting.ALL_SIMS_FORCE_AS_MALE,
                    CGSStringId.MALE,
                    CGSStringId.FEMALE,
                    on_chosen=_on_force_all_chosen,
                    on_close=_reopen
                )
            )
        )

        def _set_all_to_vanilla_gender_options_chosen() -> None:
            for sim_info in CommonSimUtils.get_instanced_sim_info_for_all_sims_generator():
                if CommonGenderUtils.is_male(sim_info):
                    CommonSimGenderOptionUtils.update_gender_options_to_vanilla_male(sim_info)
                else:
                    CommonSimGenderOptionUtils.update_gender_options_to_vanilla_female(sim_info)
            _reopen()

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    CGSStringId.SET_ALL_SIMS_TO_VANILLA_GENDER_OPTIONS_NAME,
                    CGSStringId.SET_ALL_SIMS_TO_VANILLA_GENDER_OPTIONS_DESCRIPTION,
                    icon=CommonIconUtils.load_arrow_right_icon()
                ),
                on_chosen=_set_all_to_vanilla_gender_options_chosen
            )
        )

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    CGSStringId.ALL_MALE_SIM_OPTIONS,
                    CGSStringId.ALL_MALE_SIM_OPTIONS_DESCRIPTION,
                    icon=CommonIconUtils.load_arrow_navigate_into_icon()
                ),
                on_chosen=lambda *_, **__: self._all_male_options(on_close=_reopen)
            )
        )

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    CGSStringId.ALL_FEMALE_SIM_OPTIONS,
                    CGSStringId.ALL_FEMALE_SIM_OPTIONS_DESCRIPTION,
                    icon=CommonIconUtils.load_arrow_navigate_into_icon()
                ),
                on_chosen=lambda *_, **__: self._all_female_options(on_close=_reopen)
            )
        )

        option_dialog.show()

    def _all_male_options(self, on_close: Callable[[], Any]=None):
        def _on_close() -> None:
            if on_close is not None:
                on_close()

        def _reopen() -> None:
            self._all_male_options(on_close=on_close)

        option_dialog = CommonChooseObjectOptionDialog(
            CGSStringId.ALL_MALE_SIM_OPTIONS,
            CGSStringId.ALL_MALE_SIM_OPTIONS_DESCRIPTION,
            mod_identity=self.mod_identity,
            on_close=_on_close
        )

        @CommonExceptionHandler.catch_exceptions(self.mod_identity)
        def _on_chosen(_: str, picked_option: Union[int, bool]):
            if picked_option is None:
                return
            if picked_option == -1:
                self._data_store.set_value_by_key(_, None)
                _reopen()
                return

            @CommonExceptionHandler.catch_exceptions(self.mod_identity)
            def _on_ok(_d) -> None:
                self._data_store.set_value_by_key(_, picked_option)

                for sim_info in CommonSimUtils.get_instanced_sim_info_for_all_sims_generator():
                    _CGSUpdateGenderOptions()._update_gender_options(sim_info)
                _reopen()

            @CommonExceptionHandler.catch_exceptions(self.mod_identity)
            def _on_cancel(_d) -> None:
                _reopen()

            CommonOkCancelDialog(
                CGSStringId.PLEASE_CONFIRM_NAME,
                CGSStringId.PLEASE_CONFIRM_DESCRIPTION,
                ok_text_identifier=CGSStringId.YES_UPDATE_ALL_SIMS,
                cancel_text_identifier=CGSStringId.NO
            ).show(
                on_ok_selected=_on_ok,
                on_cancel_selected=_on_cancel
            )

        self._add_picker_option(
            option_dialog,
            CGSStringId.CGS_CAN_USE_TOILET_STANDING_NAME,
            CGSStringId.GENDER_OPTION_DESCRIPTION,
            CGSGlobalSetting.ALL_MALE_SIMS_USE_TOILET_STANDING,
            CGSStringId.YES,
            CGSStringId.NO,
            on_chosen=_on_chosen,
            on_close=on_close
        )

        self._add_picker_option(
            option_dialog,
            CGSStringId.CGS_CAN_USE_TOILET_SITTING_NAME,
            CGSStringId.GENDER_OPTION_DESCRIPTION,
            CGSGlobalSetting.ALL_MALE_SIMS_USE_TOILET_SITTING,
            CGSStringId.YES,
            CGSStringId.NO,
            on_chosen=_on_chosen,
            on_close=on_close
        )

        self._add_picker_option(
            option_dialog,
            CGSStringId.BREASTS_STRING,
            CGSStringId.GENDER_OPTION_DESCRIPTION,
            CGSGlobalSetting.ALL_MALE_SIMS_BREASTS,
            CGSStringId.ON,
            CGSStringId.OFF,
            on_chosen=_on_chosen,
            on_close=on_close
        )

        self._add_picker_option(
            option_dialog,
            CGSStringId.CLOTHING_PREFERENCE_STRING_NAME,
            CGSStringId.GENDER_OPTION_DESCRIPTION,
            CGSGlobalSetting.ALL_MALE_SIMS_PREFER_MENSWEAR,
            CGSStringId.PREFER_MENSWEAR,
            CGSStringId.PREFER_WOMENSWEAR,
            on_chosen=_on_chosen,
            on_close=on_close
        )

        self._add_picker_option(
            option_dialog,
            CGSStringId.BODY_FRAME_STRING,
            CGSStringId.GENDER_OPTION_DESCRIPTION,
            CGSGlobalSetting.ALL_MALE_SIMS_HAVE_MASCULINE_FRAME,
            CGSStringId.MASCULINE,
            CGSStringId.FEMININE,
            on_chosen=_on_chosen,
            on_close=on_close
        )

        self._add_picker_option(
            option_dialog,
            CGSStringId.REPRODUCTIVE_SETTINGS_STRING,
            CGSStringId.GENDER_OPTION_DESCRIPTION,
            CGSGlobalSetting.ALL_MALE_SIMS_CAN_REPRODUCE,
            CGSStringId.CAN_REPRODUCE,
            CGSStringId.CANNOT_REPRODUCE,
            on_chosen=_on_chosen,
            on_close=on_close
        )

        self._add_picker_option(
            option_dialog,
            CGSStringId.IMPREGNATE_OTHERS_STRING,
            CGSStringId.GENDER_OPTION_DESCRIPTION,
            CGSGlobalSetting.ALL_MALE_SIMS_CAN_IMPREGNATE,
            CGSStringId.CAN_IMPREGNATE,
            CGSStringId.CANNOT_IMPREGNATE,
            on_chosen=_on_chosen,
            on_close=on_close
        )

        self._add_picker_option(
            option_dialog,
            CGSStringId.IMPREGNATED_BY_OTHERS_STRINGS,
            CGSStringId.GENDER_OPTION_DESCRIPTION,
            CGSGlobalSetting.ALL_MALE_SIMS_CAN_BE_IMPREGNATED,
            CGSStringId.CAN_BE_IMPREGNATED,
            CGSStringId.CANNOT_BE_IMPREGNATED,
            on_chosen=_on_chosen,
            on_close=on_close
        )

        option_dialog.show()

    def _all_female_options(self, on_close: Callable[[], Any]=None):
        def _on_close() -> None:
            if on_close is not None:
                on_close()

        def _reopen() -> None:
            self._all_female_options(on_close=on_close)

        option_dialog = CommonChooseObjectOptionDialog(
            CGSStringId.ALL_FEMALE_SIM_OPTIONS,
            CGSStringId.ALL_FEMALE_SIM_OPTIONS_DESCRIPTION,
            mod_identity=self.mod_identity,
            on_close=_on_close
        )

        @CommonExceptionHandler.catch_exceptions(self.mod_identity)
        def _on_chosen(_: str, picked_option: bool):
            if picked_option is None:
                return
            if picked_option == -1:
                self._data_store.set_value_by_key(_, None)
                _reopen()
                return

            def _on_ok(_d) -> None:
                self._data_store.set_value_by_key(_, picked_option)

                for sim_info in CommonSimUtils.get_instanced_sim_info_for_all_sims_generator():
                    _CGSUpdateGenderOptions()._update_gender_options(sim_info)
                _reopen()

            def _on_cancel(_d) -> None:
                _reopen()

            CommonOkCancelDialog(
                CGSStringId.PLEASE_CONFIRM_NAME,
                CGSStringId.PLEASE_CONFIRM_DESCRIPTION,
                ok_text_identifier=CGSStringId.YES_UPDATE_ALL_SIMS,
                cancel_text_identifier=CGSStringId.NO
            ).show(
                on_ok_selected=_on_ok,
                on_cancel_selected=_on_cancel
            )

        self._add_picker_option(
            option_dialog,
            CGSStringId.CGS_CAN_USE_TOILET_STANDING_NAME,
            CGSStringId.GENDER_OPTION_DESCRIPTION,
            CGSGlobalSetting.ALL_FEMALE_SIMS_USE_TOILET_STANDING,
            CGSStringId.YES,
            CGSStringId.NO,
            on_chosen=_on_chosen,
            on_close=on_close
        )

        self._add_picker_option(
            option_dialog,
            CGSStringId.CGS_CAN_USE_TOILET_SITTING_NAME,
            CGSStringId.GENDER_OPTION_DESCRIPTION,
            CGSGlobalSetting.ALL_FEMALE_SIMS_USE_TOILET_SITTING,
            CGSStringId.YES,
            CGSStringId.NO,
            on_chosen=_on_chosen,
            on_close=on_close
        )

        self._add_picker_option(
            option_dialog,
            CGSStringId.BREASTS_STRING,
            CGSStringId.GENDER_OPTION_DESCRIPTION,
            CGSGlobalSetting.ALL_FEMALE_SIMS_BREASTS,
            CGSStringId.ON,
            CGSStringId.OFF,
            on_chosen=_on_chosen,
            on_close=on_close
        )

        self._add_picker_option(
            option_dialog,
            CGSStringId.CLOTHING_PREFERENCE_STRING_NAME,
            CGSStringId.GENDER_OPTION_DESCRIPTION,
            CGSGlobalSetting.ALL_FEMALE_SIMS_PREFER_MENSWEAR,
            CGSStringId.PREFER_MENSWEAR,
            CGSStringId.PREFER_WOMENSWEAR,
            on_chosen=_on_chosen,
            on_close=on_close
        )

        self._add_picker_option(
            option_dialog,
            CGSStringId.BODY_FRAME_STRING,
            CGSStringId.GENDER_OPTION_DESCRIPTION,
            CGSGlobalSetting.ALL_FEMALE_SIMS_HAVE_MASCULINE_FRAME,
            CGSStringId.MASCULINE,
            CGSStringId.FEMININE,
            on_chosen=_on_chosen,
            on_close=on_close
        )

        self._add_picker_option(
            option_dialog,
            CGSStringId.REPRODUCTIVE_SETTINGS_STRING,
            CGSStringId.GENDER_OPTION_DESCRIPTION,
            CGSGlobalSetting.ALL_FEMALE_SIMS_CAN_REPRODUCE,
            CGSStringId.CAN_REPRODUCE,
            CGSStringId.CANNOT_REPRODUCE,
            on_chosen=_on_chosen,
            on_close=on_close
        )

        self._add_picker_option(
            option_dialog,
            CGSStringId.IMPREGNATE_OTHERS_STRING,
            CGSStringId.GENDER_OPTION_DESCRIPTION,
            CGSGlobalSetting.ALL_FEMALE_SIMS_CAN_IMPREGNATE,
            CGSStringId.CAN_IMPREGNATE,
            CGSStringId.CANNOT_IMPREGNATE,
            on_chosen=_on_chosen,
            on_close=on_close
        )

        self._add_picker_option(
            option_dialog,
            CGSStringId.IMPREGNATED_BY_OTHERS_STRINGS,
            CGSStringId.GENDER_OPTION_DESCRIPTION,
            CGSGlobalSetting.ALL_FEMALE_SIMS_CAN_BE_IMPREGNATED,
            CGSStringId.CAN_BE_IMPREGNATED,
            CGSStringId.CANNOT_BE_IMPREGNATED,
            on_chosen=_on_chosen,
            on_close=on_close
        )

        option_dialog.show()

    def _add_picker_option(
        self,
        option_dialog: CommonChooseObjectOptionDialog,
        title: int,
        description: LocalizedString,
        setting_name: str,
        on_name: int,
        off_name: int,
        on_chosen: Callable[[str, Union[bool, int]], Any],
        on_close: Callable[[], Any]
    ):
        current_val = self._data_store.get_value_by_key(setting_name)
        selected_string = CGSStringId.DISABLED
        if current_val is True:
            selected_string = on_name
        elif current_val is False:
            selected_string = off_name

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    title,
                    description,
                    title_tokens=(selected_string,)
                ),
                on_chosen=lambda *_, **__: self._select_option(
                    title,
                    description,
                    selected_string,
                    setting_name,
                    on_name,
                    off_name,
                    on_chosen=on_chosen,
                    on_close=on_close
                )
            )
        )

    def _select_option(
        self,
        title: int,
        description: LocalizedString,
        current_string: int,
        setting_name: str,
        on_name: int,
        off_name: int,
        on_chosen: Callable[[str, Union[bool, int]], Any],
        on_close: Callable[[], Any]=None
    ):
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
        def _on_chosen(_: str, picked_option: bool):
            if picked_option is None:
                _on_close()
                return
            on_chosen(_, picked_option)

        option_dialog.add_option(
            CommonDialogSelectOption(
                setting_name,
                -1,
                CommonDialogOptionContext(
                    CGSStringId.DISABLED,
                    0,
                    icon=CommonIconUtils.load_filled_circle_icon() if current_val is None else CommonIconUtils.load_unfilled_circle_icon()
                ),
                on_chosen=_on_chosen
            )
        )

        option_dialog.add_option(
            CommonDialogSelectOption(
                setting_name,
                True,
                CommonDialogOptionContext(
                    on_name,
                    0,
                    icon=CommonIconUtils.load_filled_circle_icon() if current_val is True else CommonIconUtils.load_unfilled_circle_icon()
                ),
                on_chosen=_on_chosen
            )
        )

        option_dialog.add_option(
            CommonDialogSelectOption(
                setting_name,
                False,
                CommonDialogOptionContext(
                    off_name,
                    0,
                    icon=CommonIconUtils.load_filled_circle_icon() if current_val is False else CommonIconUtils.load_unfilled_circle_icon()
                ),
                on_chosen=_on_chosen
            )
        )

        option_dialog.show()
