"""
This file is part of the Custom Gender Settings mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Any

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
from cncustomgendersettings.utils.trait_utils import CGSTraitUtils
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
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils


class CustomGenderSettingsDialog(HasLog):
    """ A Dialog that opens custom gender settings. """
    def __init__(self, on_close: Callable[..., Any]=CommonFunctionUtils.noop):
        super().__init__()
        self._on_close = on_close
        self._cgs_trait_utils = CGSTraitUtils()

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
        if CommonTraitUtils.has_masculine_frame(sim_info):
            current_body_frame = CommonStringId.MASCULINE

        def _reopen_dialog():
            self.open(sim_info)

        option_dialog = CommonChooseObjectOptionDialog(
            CommonStringId.CUSTOM_GENDER_SETTINGS,
            CGSStringId.CGS_CUSTOM_GENDER_SETTINGS_DESCRIPTION,
            mod_identity=ModInfo.get_identity(),
            on_close=_on_close
        )

        def _on_physical_frame_chosen():
            self._flip_traits_and_update_outfits(
                sim_info,
                CommonTraitId.GENDER_OPTIONS_FRAME_MASCULINE,
                CommonTraitId.GENDER_OPTIONS_FRAME_FEMININE
            )
            _reopen_dialog()

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
        if CommonTraitUtils.prefers_menswear(sim_info):
            current_clothing = CommonStringId.MASCULINE

        def _on_clothing_preference_chosen():
            self._flip_traits_and_update_outfits(
                sim_info,
                CommonTraitId.GENDER_OPTIONS_CLOTHING_MENS_WEAR,
                CommonTraitId.GENDER_OPTIONS_CLOTHING_WOMENS_WEAR
            )
            _reopen_dialog()

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
                _reopen_dialog()

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
            self._flip_traits_and_update_outfits(
                sim_info,
                CommonTraitId.GENDER_OPTIONS_TOILET_STANDING,
                CommonTraitId.GENDER_OPTIONS_TOILET_SITTING
            )
            _reopen_dialog()

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
            self._flip_traits_and_update_outfits(
                sim_info,
                CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_REPRODUCE,
                CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_NOT_REPRODUCE
            )
            self.open(sim_info)

        option_dialog = CommonChooseObjectOptionDialog(
            CommonStringId.CUSTOM_GENDER_SETTINGS,
            CGSStringId.CGS_CUSTOM_GENDER_SETTINGS_DESCRIPTION,
            mod_identity=ModInfo.get_identity(),
            on_close=_on_close
        )

        current_selected = CGSStringId.NATURAL
        has_trait = CommonTraitUtils.has_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_NOT_REPRODUCE)
        if has_trait:
            current_selected = CGSStringId.FIXED

        option_dialog.add_option(
            CommonDialogToggleOption(
                'Reproductive Settings',
                has_trait,
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
            self._cgs_trait_utils.flip_traits(
                sim_info,
                CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE,
                CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE
            )
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
            self._cgs_trait_utils.flip_traits(
                sim_info,
                CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED,
                CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED
            )
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

    def _flip_traits_and_update_outfits(self, sim_info: SimInfo, trait_one: int, trait_two: int) -> bool:
        # Has Trait One
        if CommonTraitUtils.swap_traits(sim_info, trait_one, trait_two):
            CommonOutfitUtils.update_outfits(sim_info)
            return True
        return False
