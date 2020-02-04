"""
This file is part of the Custom Gender Settings mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple
from sims.sim_info import SimInfo
from ui.ui_dialog_picker import ObjectPickerRow
from cncustomgendersettings.modinfo import ModInfo
from cncustomgendersettings.enums.strings_enum import CGSStringId
from cncustomgendersettings.utils.trait_utils import CGSTraitUtils
from sims4communitylib.dialogs.choose_item_dialog import CommonChooseItemDialog, CommonChooseItemResult
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils

log = CommonLogRegistry.get().register_log(ModInfo.get_identity().name, 'custom_gender_settings_dialog')


class CustomGenderSettingsDialog:
    """ A Dialog that handles custom gender settings. """
    @classmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name)
    def open_custom_gender_settings(cls, sim_info: SimInfo):
        """ Open the dialog for changing custom gender settings. """
        physical_frame_option_id = 10
        clothing_preference_option_id = 11
        pregnancy_option_id = 20
        toilet_stance_option_id = 21

        picker_options = list()
        current_body_frame = CommonStringId.FEMININE
        if CommonTraitUtils.has_masculine_frame(sim_info):
            current_body_frame = CommonStringId.MASCULINE
        picker_options.append(
            ObjectPickerRow(
                option_id=physical_frame_option_id,
                name=CommonLocalizationUtils.create_localized_string(CommonStringId.PHYSICAL_FRAME),
                row_description=CommonLocalizationUtils.create_localized_string(
                    CGSStringId.CGS_CURRENT,
                    tokens=(CommonLocalizationUtils.create_localized_string(current_body_frame),)
                ),
                row_tooltip=None,
                icon=CommonIconUtils.load_arrow_right_icon(),
                tag=physical_frame_option_id
            )
        )

        current_clothing = CommonStringId.FEMININE
        if CommonTraitUtils.prefers_menswear(sim_info):
            current_clothing = CommonStringId.MASCULINE
        picker_options.append(
            ObjectPickerRow(
                option_id=clothing_preference_option_id,
                name=CommonLocalizationUtils.create_localized_string(CommonStringId.CLOTHING_PREFERENCE),
                row_description=CommonLocalizationUtils.create_localized_string(
                    CGSStringId.CGS_CURRENT,
                    tokens=(CommonLocalizationUtils.create_localized_string(current_clothing),)
                ),
                row_tooltip=None,
                icon=CommonIconUtils.load_arrow_right_icon(),
                tag=clothing_preference_option_id
            )
        )

        picker_options.append(
            ObjectPickerRow(
                option_id=pregnancy_option_id,
                name=CommonLocalizationUtils.create_localized_string(CGSStringId.CGS_PREGNANCY_OPTIONS_NAME),
                row_description=CommonLocalizationUtils.create_localized_string(
                    CGSStringId.CGS_PREGNANCY_OPTIONS_DESCRIPTION
                ),
                row_tooltip=None,
                icon=CommonIconUtils.load_arrow_navigate_into_icon(),
                tag=pregnancy_option_id
            )
        )

        title = CGSStringId.CGS_TOGGLE_CAN_USE_TOILET_STANDING_NAME
        if CommonTraitUtils.uses_toilet_standing(sim_info):
            title = CommonLocalizationUtils.create_localized_string(title, text_color=CommonLocalizedStringColor.GREEN)
            icon = CommonIconUtils.load_checked_square_icon()
        else:
            icon = CommonIconUtils.load_unchecked_square_icon()
        text = CGSStringId.CGS_TOGGLE_CAN_USE_TOILET_STANDING_DESCRIPTION
        picker_options.append(
            ObjectPickerRow(
                option_id=toilet_stance_option_id,
                name=CommonLocalizationUtils.create_localized_string(title),
                row_description=CommonLocalizationUtils.create_localized_string(text),
                row_tooltip=None,
                icon=icon,
                tag=toilet_stance_option_id
            )
        )

        @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name)
        def _option_picked(picked_option: int, picker_result: CommonChooseItemResult):
            if picked_option is None or CommonChooseItemResult.is_error(picker_result):
                return
            if picked_option == physical_frame_option_id:
                CustomGenderSettingsDialog._flip_traits_and_update_outfits(
                    sim_info,
                    CommonTraitId.GENDER_OPTIONS_FRAME_MASCULINE,
                    CommonTraitId.GENDER_OPTIONS_FRAME_FEMININE
                )
            elif picked_option == clothing_preference_option_id:
                CustomGenderSettingsDialog._flip_traits_and_update_outfits(
                    sim_info,
                    CommonTraitId.GENDER_OPTIONS_CLOTHING_MENS_WEAR,
                    CommonTraitId.GENDER_OPTIONS_CLOTHING_WOMENS_WEAR
                )
            elif picked_option == pregnancy_option_id:
                CustomGenderSettingsDialog.open_pregnancy_options(sim_info)
                return
            elif picked_option == toilet_stance_option_id:
                CustomGenderSettingsDialog._flip_traits_and_update_outfits(
                    sim_info,
                    CommonTraitId.GENDER_OPTIONS_TOILET_STANDING,
                    CommonTraitId.GENDER_OPTIONS_TOILET_SITTING
                )
            CustomGenderSettingsDialog.open_custom_gender_settings(sim_info)

        dialog = CommonChooseItemDialog(
            CommonStringId.CUSTOM_GENDER_SETTINGS,
            CGSStringId.CGS_CUSTOM_GENDER_SETTINGS_DESCRIPTION,
            tuple(picker_options)
        )
        dialog.show(on_item_chosen=_option_picked)

    @classmethod
    def open_pregnancy_options(cls, sim_info: SimInfo):
        """
            Open Custom Gender Pregnancy settings.
        """
        can_get_others_pregnant_id = 10
        can_get_pregnant_id = 11

        can_get_others_pregnant_option = CustomGenderSettingsDialog._get_trait_option(
            sim_info,
            can_get_others_pregnant_id,
            CGSStringId.CGS_CAN_GET_OTHERS_PREGNANT_NAME,
            CGSStringId.CGS_CAN_GET_OTHERS_PREGNANT_DESCRIPTION,
            CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE
        )
        can_get_pregnant_option = CustomGenderSettingsDialog._get_trait_option(
            sim_info,
            can_get_pregnant_id,
            CGSStringId.CGS_CAN_BECOME_PREGNANT_NAME,
            CGSStringId.CGS_CAN_BECOME_PREGNANT_DESCRIPTION,
            CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED
        )

        @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name)
        def _option_chosen(picked_option: int, picker_result: CommonChooseItemResult):
            if picked_option is None or picker_result == CommonChooseItemResult.DIALOG_CANCELLED:
                CustomGenderSettingsDialog.open_custom_gender_settings(sim_info)
                return
            if picked_option == can_get_others_pregnant_id:
                CGSTraitUtils.flip_traits(
                    sim_info,
                    CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE,
                    CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE
                )
            elif picked_option == can_get_pregnant_id:
                CGSTraitUtils.flip_traits(
                    sim_info,
                    CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED,
                    CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED
                )
            CustomGenderSettingsDialog.open_pregnancy_options(sim_info)

        picker_rows: Tuple[ObjectPickerRow] = [can_get_others_pregnant_option, can_get_pregnant_option]
        dialog = CommonChooseItemDialog(
            CGSStringId.CGS_PREGNANCY_OPTIONS_NAME,
            CGSStringId.CGS_PREGNANCY_OPTIONS_DESCRIPTION,
            tuple(picker_rows)
        )
        dialog.show(on_item_chosen=_option_chosen)

    @staticmethod
    def _get_trait_option(
            sim_info: SimInfo,
            option_id: int,
            option_name_id: int,
            option_description_id: int,
            trait: int
    ) -> ObjectPickerRow:
        name = CommonLocalizationUtils.create_localized_string(option_name_id)
        if CommonTraitUtils.has_trait(sim_info, trait):
            name = CommonLocalizationUtils.create_localized_string(name, text_color=CommonLocalizedStringColor.GREEN)
            icon = CommonIconUtils.load_checked_square_icon()
        else:
            icon = CommonIconUtils.load_unchecked_square_icon()
        return ObjectPickerRow(
            option_id=option_id,
            name=name,
            row_description=CommonLocalizationUtils.create_localized_string(option_description_id),
            row_tooltip=None,
            icon=icon,
            tag=option_id
        )

    @classmethod
    def _flip_traits_and_update_outfits(cls, sim_info: SimInfo, trait_one: int, trait_two: int) -> bool:
        # Has Trait One
        if CGSTraitUtils.flip_traits(sim_info, trait_one, trait_two):
            CommonOutfitUtils.update_outfits(sim_info)
            return True
        return False
