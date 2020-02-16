"""
This file is part of the Custom Gender Settings mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
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
from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils

log = CommonLogRegistry.get().register_log(ModInfo.get_identity().name, 'cgs_dialog')


class CustomGenderSettingsDialog:
    """ A Dialog that handles custom gender settings. """
    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name)
    def open_custom_gender_settings(sim_info: SimInfo):
        """ Open the dialog for changing custom gender settings. """
        current_body_frame = CommonStringId.FEMININE
        if CommonTraitUtils.has_masculine_frame(sim_info):
            current_body_frame = CommonStringId.MASCULINE

        def _reopen_dialog():
            CustomGenderSettingsDialog.open_custom_gender_settings(sim_info)

        option_dialog = CommonChooseObjectOptionDialog(
            CommonStringId.CUSTOM_GENDER_SETTINGS,
            CGSStringId.CGS_CUSTOM_GENDER_SETTINGS_DESCRIPTION,
            mod_identity=ModInfo.get_identity()
        )

        def _on_physical_frame_chosen():
            CustomGenderSettingsDialog._flip_traits_and_update_outfits(
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
            CustomGenderSettingsDialog._flip_traits_and_update_outfits(
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

        def _on_pregnancy_option_chosen():
            CustomGenderSettingsDialog.open_pregnancy_options(sim_info)

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
            CustomGenderSettingsDialog._flip_traits_and_update_outfits(
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

        option_dialog.show(sim_info=sim_info)

    @staticmethod
    def open_pregnancy_options(sim_info: SimInfo):
        """
            Open Custom Gender Pregnancy settings.
        """
        can_get_others_pregnant_id = 10
        can_get_pregnant_id = 11

        def _on_close():
            CustomGenderSettingsDialog.open_custom_gender_settings(sim_info)

        def _reopen_dialog():
            CustomGenderSettingsDialog.open_pregnancy_options(sim_info)

        option_dialog = CommonChooseObjectOptionDialog(
            CGSStringId.CGS_PREGNANCY_OPTIONS_NAME,
            CGSStringId.CGS_PREGNANCY_OPTIONS_DESCRIPTION,
            mod_identity=ModInfo.get_identity(),
            on_close=_on_close
        )

        def _can_get_others_pregnant_chosen(option_identifier: str, can_get_others_pregnant: bool):
            log.format(option_identifier=option_identifier, can_get_others_pregnant=can_get_others_pregnant)
            CGSTraitUtils.flip_traits(
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
            log.format(option_identifier=option_identifier, can_get_pregnant=can_get_pregnant)
            CGSTraitUtils.flip_traits(
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

        option_dialog.show(sim_info=sim_info)

    @staticmethod
    def _flip_traits_and_update_outfits(sim_info: SimInfo, trait_one: int, trait_two: int) -> bool:
        # Has Trait One
        if CGSTraitUtils.flip_traits(sim_info, trait_one, trait_two):
            CommonOutfitUtils.update_outfits(sim_info)
            return True
        return False
