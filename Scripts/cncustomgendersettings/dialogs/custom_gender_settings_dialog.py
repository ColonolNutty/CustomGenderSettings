"""
This file is part of the Custom Gender Settings mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Any

from cncustomgendersettings.persistence.cgs_sim_data import CGSSimData
from cncustomgendersettings.settings.dialog import CGSGlobalSettingsDialog
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_ok_dialog import CommonOkDialog
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_action_option import \
    CommonDialogActionOption
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_toggle_option import \
    CommonDialogToggleOption
from cncustomgendersettings.modinfo import ModInfo
from cncustomgendersettings.enums.strings_enum import CGSStringId
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils

debug = False


class CustomGenderSettingsDialog(HasLog):
    """ A Dialog that opens custom gender settings. """
    def __init__(self, sim_info: SimInfo, on_close: Callable[..., Any]=CommonFunctionUtils.noop):
        super().__init__()
        self._sim_info = sim_info
        self._on_close = on_close

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cgs_dialog'

    def open(self):
        """ Open the dialog. """
        try:
            def _on_close() -> None:
                if self._on_close is not None:
                    self._on_close()

            if CommonSpeciesUtils.is_pet(self._sim_info):
                self._settings_pet(on_close=_on_close)
            else:
                self._settings_human(on_close=_on_close)
        except Exception as ex:
            self.log.error('Error occurred while opening custom gender settings dialog.', exception=ex)

    def _settings_human(self, on_close: Callable[[], Any]=None) -> None:
        def _on_close() -> None:
            if on_close is not None:
                on_close()

        def _reopen():
            self._settings_human(on_close=on_close)

        option_dialog = CommonChooseObjectOptionDialog(
            CommonStringId.CUSTOM_GENDER_SETTINGS,
            CGSStringId.CGS_CUSTOM_GENDER_SETTINGS_DESCRIPTION,
            mod_identity=self.mod_identity,
            on_close=_on_close
        )

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    CGSStringId.GLOBAL_SETTINGS_NAME,
                    CGSStringId.GLOBAL_SETTINGS_DESCRIPTION
                ),
                on_chosen=CGSGlobalSettingsDialog(self._sim_info, on_close=_reopen).open
            )
        )

        if debug:
            def _reset_to_original_gender_chosen():
                CGSSimData(self._sim_info).reset_to_original_gender_and_gender_options()
                _reopen()

            option_dialog.add_option(
                CommonDialogActionOption(
                    CommonDialogOptionContext(
                        CGSStringId.CGS_RESET_TO_ORIGINAL_GENDER_NAME,
                        CGSStringId.CGS_RESET_TO_ORIGINAL_GENDER_DESCRIPTION,
                        icon=CommonIconUtils.load_arrow_right_icon()
                    ),
                    on_chosen=_reset_to_original_gender_chosen
                )
            )

        def _set_to_vanilla_gender_chosen():
            if CommonGenderUtils.is_male(self._sim_info):
                CommonSimGenderOptionUtils.update_gender_options_to_vanilla_male(self._sim_info)
            else:
                CommonSimGenderOptionUtils.update_gender_options_to_vanilla_female(self._sim_info)
            _reopen()

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    CGSStringId.CGS_SET_TO_VANILLA_GENDER_OPTIONS_NAME,
                    CGSStringId.CGS_SET_TO_VANILLA_GENDER_OPTIONS_DESCRIPTION,
                    icon=CommonIconUtils.load_arrow_right_icon()
                ),
                on_chosen=_set_to_vanilla_gender_chosen
            )
        )

        def _on_gender_chosen():
            CommonGenderUtils.swap_gender(self._sim_info, update_gender_options=False)
            CGSSimData(self._sim_info).original_gender = CommonGenderUtils.get_gender(self._sim_info)
            _reopen()

        current_gender_string = CGSStringId.MALE
        if CommonGenderUtils.is_female(self._sim_info):
            current_gender_string = CGSStringId.FEMALE

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    CGSStringId.CGS_SWAP_GENDER_NAME,
                    CGSStringId.CGS_SWAP_GENDER_DESCRIPTION,
                    title_tokens=(current_gender_string,),
                    icon=CommonIconUtils.load_arrow_right_icon()
                ),
                on_chosen=_on_gender_chosen
            )
        )

        def _on_physical_frame_chosen():
            value = not CommonSimGenderOptionUtils.has_masculine_frame(self._sim_info)
            CommonSimGenderOptionUtils.update_body_frame(self._sim_info, value)
            CGSSimData(self._sim_info).original_has_masculine_frame = value
            _reopen()

        current_body_frame = CommonStringId.FEMININE
        if CommonSimGenderOptionUtils.has_masculine_frame(self._sim_info):
            current_body_frame = CommonStringId.MASCULINE

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    CommonStringId.PHYSICAL_FRAME,
                    CGSStringId.CGS_CURRENT,
                    description_tokens=(current_body_frame,),
                    icon=CommonIconUtils.load_arrow_right_icon()
                ),
                on_chosen=_on_physical_frame_chosen
            )
        )

        current_clothing = CommonStringId.FEMININE
        if CommonSimGenderOptionUtils.prefers_menswear(self._sim_info):
            current_clothing = CommonStringId.MASCULINE

        def _on_clothing_preference_chosen():
            value = not CommonSimGenderOptionUtils.prefers_menswear(self._sim_info)
            CommonSimGenderOptionUtils.update_clothing_preference(self._sim_info, value)
            CGSSimData(self._sim_info).original_prefers_menswear = value
            _reopen()

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    CommonStringId.CLOTHING_PREFERENCE,
                    CGSStringId.CGS_CURRENT,
                    description_tokens=(current_clothing,),
                    icon=CommonIconUtils.load_arrow_right_icon()
                ),
                on_chosen=_on_clothing_preference_chosen
            )
        )

        def _on_toggle_breasts_chosen(option_identifier: str, has_breasts: bool):
            self.log.format(option_identifier=option_identifier, has_breasts=has_breasts)

            def _on_acknowledged(_):
                _reopen()

            CommonSimGenderOptionUtils.update_has_breasts(self._sim_info, has_breasts)
            CGSSimData(self._sim_info).original_has_breasts = has_breasts
            CommonOkDialog(
                CGSStringId.CGS_SETTING_SAVE_RELOAD_ALERT_NAME,
                CGSStringId.CGS_SETTING_SAVE_RELOAD_ALERT_DESCRIPTION
            ).show(on_acknowledged=_on_acknowledged)

        has_vanilla_breasts = False
        if CommonGenderUtils.is_female(self._sim_info):
            has_vanilla_breasts = not CommonTraitUtils.has_trait(self._sim_info, CommonTraitId.BREASTS_FORCE_OFF)

        option_dialog.add_option(
            CommonDialogToggleOption(
                'ToggleBreasts',
                CommonTraitUtils.has_trait(self._sim_info, CommonTraitId.BREASTS_FORCE_ON) or has_vanilla_breasts,
                CommonDialogOptionContext(
                    CGSStringId.CGS_TOGGLE_BREASTS_NAME,
                    CGSStringId.CGS_TOGGLE_BREASTS_DESCRIPTION
                ),
                on_chosen=_on_toggle_breasts_chosen
            )
        )

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    CGSStringId.CGS_PREGNANCY_OPTIONS_NAME,
                    CGSStringId.CGS_PREGNANCY_OPTIONS_DESCRIPTION,
                    icon=CommonIconUtils.load_arrow_navigate_into_icon()
                ),
                on_chosen=lambda *_, **__: self._pregnancy_options(on_close=_reopen)
            )
        )

        title = CGSStringId.CGS_TOGGLE_CAN_USE_TOILET_STANDING_NAME
        if CommonSimGenderOptionUtils.uses_toilet_standing(self._sim_info):
            title = CommonLocalizationUtils.create_localized_string(title, text_color=CommonLocalizedStringColor.GREEN)
            icon = CommonIconUtils.load_checked_square_icon()
        else:
            icon = CommonIconUtils.load_unchecked_square_icon()
        text = CGSStringId.CGS_TOGGLE_CAN_USE_TOILET_STANDING_DESCRIPTION

        def _on_toilet_usage_chosen():
            value = not CommonSimGenderOptionUtils.uses_toilet_standing(self._sim_info)
            CommonSimGenderOptionUtils.update_toilet_usage(self._sim_info, value)
            CGSSimData(self._sim_info).original_uses_toilet_standing = value
            _reopen()

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    title,
                    text,
                    icon=icon
                ),
                on_chosen=_on_toilet_usage_chosen
            )
        )

        option_dialog.show(sim_info=self._sim_info)

    def _settings_pet(self, on_close: Callable[[], Any]=None) -> None:
        def _reopen() -> None:
            self._settings_pet(on_close=on_close)

        def _on_close(*_, **__) -> None:
            if on_close is not None:
                on_close()

        def _on_chosen(_: str, picked_option: bool):
            if picked_option is None:
                _on_close()
                return
            value = not CommonSimGenderOptionUtils.can_reproduce(self._sim_info)
            CommonSimGenderOptionUtils.update_can_reproduce(self._sim_info, value)
            CGSSimData(self._sim_info).original_can_reproduce = value
            _reopen()

        option_dialog = CommonChooseObjectOptionDialog(
            CommonStringId.CUSTOM_GENDER_SETTINGS,
            CGSStringId.CGS_CUSTOM_GENDER_SETTINGS_DESCRIPTION,
            mod_identity=self.mod_identity,
            on_close=_on_close
        )

        if debug:
            def _reset_to_original_gender_chosen():
                CGSSimData(self._sim_info).reset_to_original_gender_and_gender_options()
                _reopen()

            option_dialog.add_option(
                CommonDialogActionOption(
                    CommonDialogOptionContext(
                        CGSStringId.CGS_RESET_TO_ORIGINAL_GENDER_NAME,
                        CGSStringId.CGS_RESET_TO_ORIGINAL_GENDER_DESCRIPTION,
                        icon=CommonIconUtils.load_arrow_right_icon()
                    ),
                    on_chosen=_reset_to_original_gender_chosen
                )
            )

        current_selected = CGSStringId.NATURAL
        can_reproduce = CommonSimGenderOptionUtils.can_reproduce(self._sim_info)
        if not can_reproduce:
            current_selected = CGSStringId.FIXED

        option_dialog.add_option(
            CommonDialogToggleOption(
                'Reproductive Settings',
                can_reproduce,
                CommonDialogOptionContext(
                    CGSStringId.REPRODUCTIVE_SETTINGS,
                    CGSStringId.CGS_CURRENT,
                    description_tokens=(current_selected,),
                    icon=CommonIconUtils.load_question_mark_icon()
                ),
                on_chosen=_on_chosen
            )
        )

        option_dialog.show(sim_info=self._sim_info)

    def _pregnancy_options(self, on_close: Callable[[], Any]=None) -> None:
        def _on_close():
            if on_close is not None:
                on_close()

        def _reopen():
            self._pregnancy_options(on_close=on_close)

        option_dialog = CommonChooseObjectOptionDialog(
            CGSStringId.CGS_PREGNANCY_OPTIONS_NAME,
            CGSStringId.CGS_PREGNANCY_OPTIONS_DESCRIPTION,
            mod_identity=self.mod_identity,
            on_close=_on_close
        )

        def _can_impregnate_chosen(option_identifier: str, can_get_others_pregnant: bool):
            self.log.format(option_identifier=option_identifier, can_get_others_pregnant=can_get_others_pregnant)
            value = not CommonSimGenderOptionUtils.can_impregnate(self._sim_info)
            CommonSimGenderOptionUtils.update_can_impregnate(self._sim_info, value)
            CGSSimData(self._sim_info).original_can_impregnate = value
            _reopen()

        option_dialog.add_option(
            CommonDialogToggleOption(
                'CanImpregnate',
                CommonSimGenderOptionUtils.can_impregnate(self._sim_info),
                CommonDialogOptionContext(
                    CGSStringId.CGS_CAN_GET_OTHERS_PREGNANT_NAME,
                    CGSStringId.CGS_CAN_GET_OTHERS_PREGNANT_DESCRIPTION
                ),
                on_chosen=_can_impregnate_chosen
            )
        )

        def _can_be_impregnated_chosen(option_identifier: str, can_get_pregnant: bool):
            self.log.format(option_identifier=option_identifier, can_get_pregnant=can_get_pregnant)
            value = not CommonSimGenderOptionUtils.can_be_impregnated(self._sim_info)
            CommonSimGenderOptionUtils.update_can_be_impregnated(self._sim_info, value)
            CGSSimData(self._sim_info).original_can_be_impregnated = value
            _reopen()

        option_dialog.add_option(
            CommonDialogToggleOption(
                'CanBeImpregnated',
                CommonSimGenderOptionUtils.can_be_impregnated(self._sim_info),
                CommonDialogOptionContext(
                    CGSStringId.CGS_CAN_BECOME_PREGNANT_NAME,
                    CGSStringId.CGS_CAN_BECOME_PREGNANT_DESCRIPTION
                ),
                on_chosen=_can_be_impregnated_chosen
            )
        )

        option_dialog.show(sim_info=self._sim_info)
