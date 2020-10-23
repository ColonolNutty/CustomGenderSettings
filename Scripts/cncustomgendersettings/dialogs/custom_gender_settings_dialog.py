"""
This file is part of the Custom Gender Settings mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Any

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
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils


class CustomGenderSettingsDialog(HasLog):
    """ A Dialog that opens custom gender settings. """
    def __init__(self, on_close: Callable[..., Any]=CommonFunctionUtils.noop):
        super().__init__()
        self._on_close = on_close

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cgs_dialog'

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity())
    def open(self, sim_info: SimInfo):
        """ Open the dialog for changing custom gender settings. """
        self._settings(sim_info).show(sim_info=sim_info)

    def _settings(self, sim_info: SimInfo) -> CommonChooseObjectOptionDialog:
        if CommonSpeciesUtils.is_pet(sim_info):
            return self._settings_pet(sim_info)
        return self._settings_human(sim_info)

    def _settings_human(self, sim_info: SimInfo) -> CommonChooseObjectOptionDialog:
        def _on_close() -> None:
            if self._on_close is not None:
                self._on_close()

        current_body_frame = CommonStringId.FEMININE
        if CommonSimGenderOptionUtils.has_masculine_frame(sim_info):
            current_body_frame = CommonStringId.MASCULINE

        def _reopen():
            self.open(sim_info)

        option_dialog = CommonChooseObjectOptionDialog(
            CommonStringId.CUSTOM_GENDER_SETTINGS,
            CGSStringId.CGS_CUSTOM_GENDER_SETTINGS_DESCRIPTION,
            mod_identity=ModInfo.get_identity(),
            on_close=_on_close
        )

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    CGSStringId.GLOBAL_SETTINGS_NAME,
                    CGSStringId.GLOBAL_SETTINGS_DESCRIPTION
                ),
                on_chosen=CGSGlobalSettingsDialog(sim_info, on_close=_reopen).open
            )
        )

        def _on_physical_frame_chosen():
            CommonSimGenderOptionUtils.update_body_frame(sim_info, not CommonSimGenderOptionUtils.has_masculine_frame(sim_info))
            _reopen()

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
        if CommonSimGenderOptionUtils.prefers_menswear(sim_info):
            current_clothing = CommonStringId.MASCULINE

        def _on_clothing_preference_chosen():
            CommonSimGenderOptionUtils.update_clothing_preference(sim_info, not CommonSimGenderOptionUtils.prefers_menswear(sim_info))
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

        def _on_has_breasts_chosen(option_identifier: str, has_breasts: bool):
            self.log.format(option_identifier=option_identifier, has_breasts=has_breasts)

            def _on_acknowledged(_):
                _reopen()

            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.BREASTS_FORCE_OFF)
            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.BREASTS_FORCE_ON)
            if not has_breasts:
                if CommonGenderUtils.is_female(sim_info):
                    CommonTraitUtils.add_trait(sim_info, CommonTraitId.BREASTS_FORCE_OFF)
            else:
                if CommonGenderUtils.is_male(sim_info):
                    CommonTraitUtils.add_trait(sim_info, CommonTraitId.BREASTS_FORCE_ON)
            CommonOutfitUtils.update_outfits(sim_info)
            CommonOkDialog(
                CGSStringId.CGS_SETTING_SAVE_RELOAD_ALERT_NAME,
                CGSStringId.CGS_SETTING_SAVE_RELOAD_ALERT_DESCRIPTION
            ).show(on_acknowledged=_on_acknowledged)

        has_vanilla_breasts = False
        if CommonGenderUtils.is_female(sim_info):
            has_vanilla_breasts = not CommonTraitUtils.has_trait(sim_info, CommonTraitId.BREASTS_FORCE_OFF)

        option_dialog.add_option(
            CommonDialogToggleOption(
                'HasBreasts',
                CommonTraitUtils.has_trait(sim_info, CommonTraitId.BREASTS_FORCE_ON) or has_vanilla_breasts,
                CommonDialogOptionContext(
                    CGSStringId.CGS_TOGGLE_BREASTS_NAME,
                    CGSStringId.CGS_TOGGLE_BREASTS_DESCRIPTION
                ),
                on_chosen=_on_has_breasts_chosen
            )
        )

        def _on_pregnancy_option_chosen():
            self._pregnancy_options(sim_info).show(sim_info=sim_info)

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    CGSStringId.CGS_PREGNANCY_OPTIONS_NAME,
                    CGSStringId.CGS_PREGNANCY_OPTIONS_DESCRIPTION,
                    icon=CommonIconUtils.load_arrow_navigate_into_icon()
                ),
                on_chosen=_on_pregnancy_option_chosen
            )
        )

        title = CGSStringId.CGS_TOGGLE_CAN_USE_TOILET_STANDING_NAME
        if CommonTraitUtils.uses_toilet_standing(sim_info):
            title = CommonLocalizationUtils.create_localized_string(title, text_color=CommonLocalizedStringColor.GREEN)
            icon = CommonIconUtils.load_checked_square_icon()
        else:
            icon = CommonIconUtils.load_unchecked_square_icon()
        text = CGSStringId.CGS_TOGGLE_CAN_USE_TOILET_STANDING_DESCRIPTION

        def _on_toilet_preference_chosen():
            CommonSimGenderOptionUtils.update_toilet_usage(sim_info, not CommonSimGenderOptionUtils.uses_toilet_standing(sim_info))
            _reopen()

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    title,
                    text,
                    icon=icon
                ),
                on_chosen=_on_toilet_preference_chosen
            )
        )

        return option_dialog

    def _settings_pet(self, sim_info: SimInfo):
        def _on_close(*_, **__) -> None:
            if self._on_close is not None:
                self._on_close()

        @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity())
        def _on_chosen(_: str, picked_option: int):
            if picked_option is None:
                return
            CommonSimGenderOptionUtils.update_can_reproduce(sim_info, not CommonSimGenderOptionUtils.can_reproduce(sim_info))
            self.open(sim_info)

        option_dialog = CommonChooseObjectOptionDialog(
            CommonStringId.CUSTOM_GENDER_SETTINGS,
            CGSStringId.CGS_CUSTOM_GENDER_SETTINGS_DESCRIPTION,
            mod_identity=ModInfo.get_identity(),
            on_close=_on_close
        )

        current_selected = CGSStringId.NATURAL
        can_reproduce = CommonSimGenderOptionUtils.can_reproduce(sim_info)
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

        return option_dialog

    def _pregnancy_options(self, sim_info: SimInfo) -> CommonChooseObjectOptionDialog:
        def _on_close():
            self.open(sim_info)

        def _reopen_dialog():
            self._pregnancy_options(sim_info).show(sim_info=sim_info)

        option_dialog = CommonChooseObjectOptionDialog(
            CGSStringId.CGS_PREGNANCY_OPTIONS_NAME,
            CGSStringId.CGS_PREGNANCY_OPTIONS_DESCRIPTION,
            mod_identity=ModInfo.get_identity(),
            on_close=_on_close
        )

        def _can_get_others_pregnant_chosen(option_identifier: str, can_get_others_pregnant: bool):
            self.log.format(option_identifier=option_identifier, can_get_others_pregnant=can_get_others_pregnant)
            CommonSimGenderOptionUtils.update_can_impregnate(sim_info, not CommonSimGenderOptionUtils.can_impregnate(sim_info))
            _reopen_dialog()

        option_dialog.add_option(
            CommonDialogToggleOption(
                'CanGetOthersPregnant',
                CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE),
                CommonDialogOptionContext(
                    CGSStringId.CGS_CAN_GET_OTHERS_PREGNANT_NAME,
                    CGSStringId.CGS_CAN_GET_OTHERS_PREGNANT_DESCRIPTION
                ),
                on_chosen=_can_get_others_pregnant_chosen
            )
        )

        def _can_get_pregnant_chosen(option_identifier: str, can_get_pregnant: bool):
            self.log.format(option_identifier=option_identifier, can_get_pregnant=can_get_pregnant)
            CommonSimGenderOptionUtils.update_can_be_impregnated(sim_info, not CommonSimGenderOptionUtils.can_be_impregnated(sim_info))
            _reopen_dialog()

        option_dialog.add_option(
            CommonDialogToggleOption(
                'CanGetPregnant',
                CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED),
                CommonDialogOptionContext(
                    CGSStringId.CGS_CAN_BECOME_PREGNANT_NAME,
                    CGSStringId.CGS_CAN_BECOME_PREGNANT_DESCRIPTION
                ),
                on_chosen=_can_get_pregnant_chosen
            )
        )

        return option_dialog
