"""
Custom Gender Settings is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.global_gender_preference_tuning import GenderPreferenceType
from typing import Callable, Any, Tuple, Union

from customgendersettings.enums.trait_ids import CGSTraitId
from customgendersettings.logging.has_cgs_log import HasCGSLog
from customgendersettings.settings.dialog import CGSGlobalSettingsDialog
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.common_ok_dialog import CommonOkDialog
from sims4communitylib.dialogs.ok_cancel_dialog import CommonOkCancelDialog
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.dialogs.option_dialogs.common_choose_objects_option_dialog import CommonChooseObjectsOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_action_option import \
    CommonDialogActionOption
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_input_option import \
    CommonDialogInputFloatOption
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_select_option import \
    CommonDialogSelectOption
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_toggle_option import \
    CommonDialogToggleOption
from customgendersettings.modinfo import ModInfo
from customgendersettings.enums.strings_enum import CGSStringId
from sims4communitylib.enums.common_gender import CommonGender
from sims4communitylib.enums.common_voice_actor_type import CommonVoiceActorType
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
from sims4communitylib.utils.sims.common_sim_gender_preference_utils import CommonSimGenderPreferenceUtils
from sims4communitylib.utils.sims.common_sim_voice_utils import CommonSimVoiceUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
from ui.ui_dialog import UiDialogOkCancel


class CustomGenderSettingsDialog(HasCGSLog):
    """ A Dialog that opens custom gender settings. """
    def __init__(self, sim_info: SimInfo, on_close: Callable[[], None] = CommonFunctionUtils.noop):
        super().__init__()
        self._sim_info = sim_info
        self._on_close = on_close

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cgs_dialog'

    def open(self) -> None:
        """ Open the dialog. """
        try:
            def _on_close() -> None:
                if self._on_close is not None:
                    self._on_close()

            self._settings(on_close=_on_close)
        except Exception as ex:
            self.log.error('Error occurred while opening custom gender settings dialog.', exception=ex)

    def _settings(self, on_close: Callable[[], Any] = None) -> None:
        def _on_close() -> None:
            if on_close is not None:
                on_close()

        def _reopen() -> None:
            self._settings(on_close=on_close)

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

        def _on_toggle_global_exclude_chosen(option_identifier: str, has_trait: bool):
            self.log.format(option_identifier=option_identifier, has_trait=has_trait)
            if has_trait:
                self.log.format_with_message('Adding the trait to the Sim.', sim=self._sim_info, has_trait=has_trait)
                CommonTraitUtils.add_trait(self._sim_info, CGSTraitId.CGS_EXCLUDE_FROM_GLOBAL_OVERRIDES)
            else:
                self.log.format_with_message('Removing the trait from the Sim.', sim=self._sim_info, has_trait=has_trait)
                CommonTraitUtils.remove_trait(self._sim_info, CGSTraitId.CGS_EXCLUDE_FROM_GLOBAL_OVERRIDES)

            _reopen()

        option_dialog.add_option(
            CommonDialogToggleOption(
                'ToggleGlobalExclude',
                CommonTraitUtils.has_trait(self._sim_info, CGSTraitId.CGS_EXCLUDE_FROM_GLOBAL_OVERRIDES),
                CommonDialogOptionContext(
                    CGSStringId.EXCLUDE_THIS_SIM_FROM_GLOBAL_OVERRIDES_NAME,
                    CGSStringId.EXCLUDE_THIS_SIM_FROM_GLOBAL_OVERRIDES_DESCRIPTION
                ),
                on_chosen=_on_toggle_global_exclude_chosen
            )
        )

        def _set_to_vanilla_gender_chosen() -> None:
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

        def _on_gender_chosen() -> None:
            @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=False)
            def _on_ok(_: UiDialogOkCancel):
                CommonGenderUtils.swap_gender(self._sim_info, update_gender_options=True, update_voice=True, update_outfits=True)
                _reopen()

            @CommonExceptionHandler.catch_exceptions(self.mod_identity, fallback_return=False)
            def _on_cancel(_: UiDialogOkCancel):
                CommonGenderUtils.swap_gender(self._sim_info, update_gender_options=False, update_voice=False, update_outfits=False)
                _reopen()

            CommonOkCancelDialog(
                CGSStringId.UPDATE_GENDER_OPTIONS_TOO_QUESTION,
                CGSStringId.DO_YOU_WANT_GENDER_OPTIONS_UPDATED_TOO,
                ok_text_identifier=CommonStringId.S4CL_YES,
                cancel_text_identifier=CommonStringId.S4CL_NO,
                mod_identity=self.mod_identity
            ).show(on_ok_selected=_on_ok, on_cancel_selected=_on_cancel)

        current_gender_string = CGSStringId.MALE
        if CommonGenderUtils.is_female(self._sim_info):
            current_gender_string = CGSStringId.FEMALE

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    CGSStringId.CGS_SWAP_GENDER_NAME,
                    CGSStringId.CGS_SWAP_GENDER_DESCRIPTION,
                    title_tokens=(CommonLocalizationUtils.colorize(current_gender_string, text_color=CommonLocalizedStringColor.GREEN),),
                    icon=CommonIconUtils.load_arrow_right_icon()
                ),
                on_chosen=_on_gender_chosen
            )
        )

        if CommonSpeciesUtils.is_human(self._sim_info):
            def _on_physical_frame_chosen() -> None:
                value = not CommonSimGenderOptionUtils.has_masculine_frame(self._sim_info)
                CommonSimGenderOptionUtils.update_body_frame(self._sim_info, value)
                _reopen()

            current_body_frame_text = CommonStringId.FEMININE
            if CommonSimGenderOptionUtils.has_masculine_frame(self._sim_info):
                current_body_frame_text = CommonStringId.MASCULINE

            option_dialog.add_option(
                CommonDialogActionOption(
                    CommonDialogOptionContext(
                        CommonStringId.PHYSICAL_FRAME,
                        CommonLocalizationUtils.colorize(current_body_frame_text, text_color=CommonLocalizedStringColor.GREEN),
                        icon=CommonIconUtils.load_arrow_right_icon()
                    ),
                    on_chosen=_on_physical_frame_chosen
                )
            )

            current_clothing_text = CommonStringId.FEMININE
            if CommonSimGenderOptionUtils.prefers_menswear(self._sim_info):
                current_clothing_text = CommonStringId.MASCULINE

            def _on_clothing_preference_chosen() -> None:
                value = not CommonSimGenderOptionUtils.prefers_menswear(self._sim_info)
                CommonSimGenderOptionUtils.update_clothing_preference(self._sim_info, value)
                _reopen()

            option_dialog.add_option(
                CommonDialogActionOption(
                    CommonDialogOptionContext(
                        CommonStringId.CLOTHING_PREFERENCE,
                        CommonLocalizationUtils.colorize(current_clothing_text, text_color=CommonLocalizedStringColor.GREEN),
                        icon=CommonIconUtils.load_arrow_right_icon()
                    ),
                    on_chosen=_on_clothing_preference_chosen
                )
            )

            def _on_toggle_breasts_chosen(option_identifier: str, _has_breasts: bool):
                self.log.format(option_identifier=option_identifier, has_breasts=_has_breasts)

                def _on_acknowledged(_) -> None:
                    _reopen()

                CommonSimGenderOptionUtils.update_has_breasts(self._sim_info, _has_breasts)
                CommonOkDialog(
                    CGSStringId.CGS_SETTING_SAVE_RELOAD_ALERT_NAME,
                    CGSStringId.CGS_SETTING_SAVE_RELOAD_ALERT_DESCRIPTION
                ).show(on_acknowledged=_on_acknowledged)

            has_vanilla_breasts = False
            if CommonGenderUtils.is_female(self._sim_info):
                has_vanilla_breasts = not CommonTraitUtils.has_trait(self._sim_info, CommonTraitId.BREASTS_FORCE_OFF)

            has_breasts = CommonTraitUtils.has_trait(self._sim_info, CommonTraitId.BREASTS_FORCE_ON) or has_vanilla_breasts

            option_dialog.add_option(
                CommonDialogToggleOption(
                    'ToggleBreasts',
                    has_breasts,
                    CommonDialogOptionContext(
                        CGSStringId.CGS_HAS_BREASTS,
                        CommonLocalizationUtils.colorize(CommonStringId.S4CL_YES if has_breasts else CommonStringId.S4CL_NO, text_color=CommonLocalizedStringColor.GREEN)
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

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    CGSStringId.CGS_SEXUAL_ORIENTATION_OPTIONS_NAME,
                    CGSStringId.CGS_SEXUAL_ORIENTATION_OPTIONS_DESCRIPTION,
                    icon=CommonIconUtils.load_arrow_navigate_into_icon()
                ),
                on_chosen=lambda *_, **__: self._sexual_orientation_options(on_close=_reopen)
            )
        )

        def _on_can_use_toilet_standing_chosen(_: str, can_use_toilet_standing: bool):
            CommonSimGenderOptionUtils.set_can_use_toilet_standing(self._sim_info, can_use_toilet_standing)
            _reopen()

        option_dialog.add_option(
            CommonDialogToggleOption(
                'CanUseToiletStanding',
                CommonSimGenderOptionUtils.uses_toilet_standing(self._sim_info),
                CommonDialogOptionContext(
                    CGSStringId.CGS_CAN_USE_TOILET_STANDING_NAME,
                    CGSStringId.CGS_CAN_USE_TOILET_STANDING_DESCRIPTION,
                    title_tokens=(
                        CommonLocalizationUtils.colorize(CommonStringId.S4CL_YES if CommonSimGenderOptionUtils.uses_toilet_standing(self._sim_info) else CommonStringId.S4CL_NO, text_color=CommonLocalizedStringColor.GREEN),
                    )
                ),
                on_chosen=_on_can_use_toilet_standing_chosen
            )
        )

        def _on_can_use_toilet_sitting_chosen(_: str, can_use_toilet_sitting: bool):
            CommonSimGenderOptionUtils.set_can_use_toilet_sitting(self._sim_info, can_use_toilet_sitting)
            _reopen()

        option_dialog.add_option(
            CommonDialogToggleOption(
                'CanUseToiletSitting',
                CommonSimGenderOptionUtils.uses_toilet_sitting(self._sim_info),
                CommonDialogOptionContext(
                    CGSStringId.CGS_CAN_USE_TOILET_SITTING_NAME,
                    CGSStringId.CGS_CAN_USE_TOILET_SITTING_DESCRIPTION,
                    title_tokens=(
                        CommonLocalizationUtils.colorize(CommonStringId.S4CL_YES if CommonSimGenderOptionUtils.uses_toilet_sitting(self._sim_info) else CommonStringId.S4CL_NO, text_color=CommonLocalizedStringColor.GREEN),
                    )
                ),
                on_chosen=_on_can_use_toilet_sitting_chosen
            )
        )

        def _on_voice_pitch_changed(_: str, setting_value: float, outcome: CommonChoiceOutcome):
            if setting_value is None or CommonChoiceOutcome.is_error_or_cancel(outcome):
                _reopen()
                return
            CommonSimVoiceUtils.set_voice_pitch(self._sim_info, setting_value)
            _reopen()

        voice_pitch = CommonSimVoiceUtils.get_voice_pitch(self._sim_info)
        option_dialog.add_option(
            CommonDialogInputFloatOption(
                'VoicePitch',
                voice_pitch,
                CommonDialogOptionContext(
                    CGSStringId.SET_VOICE_PITCH_TITLE,
                    CGSStringId.SET_VOICE_PITCH_DESCRIPTION,
                    title_tokens=(
                        str(voice_pitch),
                    ),
                    description_tokens=(
                        '-1.0',
                        '1.0'
                    )
                ),
                min_value=-1.0,
                max_value=1.0,
                on_chosen=_on_voice_pitch_changed
            )
        )

        voice_actor = CommonSimVoiceUtils.get_voice_actor(self._sim_info)
        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    CGSStringId.SET_VOICE_ACTOR_TITLE,
                    CGSStringId.SET_VOICE_ACTOR_DESCRIPTION,
                    title_tokens=(
                        str(voice_actor.name if isinstance(voice_actor, CommonVoiceActorType) else voice_actor),
                    ),
                    icon=CommonIconUtils.load_arrow_navigate_into_icon()
                ),
                on_chosen=lambda *_, **__: self._set_voice_actor(on_close=_reopen)
            )
        )

        option_dialog.show(sim_info=self._sim_info)

    def _sexual_orientation_options(self, on_close: Callable[[], None] = None) -> None:
        def _on_close() -> None:
            if on_close is not None:
                on_close()

        def _reopen() -> None:
            self._sexual_orientation_options(on_close=on_close)

        option_dialog = CommonChooseObjectOptionDialog(
            CGSStringId.CGS_SEXUAL_ORIENTATION_OPTIONS_NAME,
            CGSStringId.CGS_SEXUAL_ORIENTATION_OPTIONS_DESCRIPTION,
            mod_identity=self.mod_identity,
            on_close=_on_close
        )
        self._build_sexual_orientation_options(option_dialog, _on_close, _reopen)

        if not option_dialog.has_options():
            _on_close()
            return

        option_dialog.show(sim_info=self._sim_info)

    def _build_sexual_orientation_options(self, option_dialog: CommonChooseObjectOptionDialog, on_close: Callable[[], None], reopen: Callable[[], None]) -> None:
        def _is_exploring_sexuality(option_identifier: str, _is_exploring_sexuality: bool):
            self.log.format(option_identifier=option_identifier, is_exploring_sexuality=_is_exploring_sexuality)
            value = not CommonSimGenderOptionUtils.is_exploring_sexuality(self._sim_info)
            CommonSimGenderOptionUtils.set_is_exploring_sexuality(self._sim_info, value)
            reopen()

        is_exploring_sexuality = CommonSimGenderOptionUtils.is_exploring_sexuality(self._sim_info)
        is_exploring_text = CommonLocalizationUtils.colorize(CommonLocalizationUtils.create_localized_string(CommonStringId.S4CL_YES if is_exploring_sexuality else CommonStringId.S4CL_NO), text_color=CommonLocalizedStringColor.GREEN)

        option_dialog.add_option(
            CommonDialogToggleOption(
                'IsExploringSexuality',
                CommonSimGenderOptionUtils.is_exploring_sexuality(self._sim_info),
                CommonDialogOptionContext(
                    CommonStringId.THIS_SIM_IS_EXPLORING_ROMANTICALLY,
                    is_exploring_text
                ),
                on_chosen=_is_exploring_sexuality
            )
        )

        preferred_romantic_genders = CommonSimGenderPreferenceUtils.determine_preferred_genders(self._sim_info, preference_type=GenderPreferenceType.ROMANTIC)
        if preferred_romantic_genders:
            preferred_romantic_gender_display_text_list = [CommonGender.convert_to_localized_string_id(gender) for gender in preferred_romantic_genders]
            preferred_romantic_gender_display_text = CommonLocalizationUtils.colorize(CommonLocalizationUtils.combine_localized_strings_with_comma_space_and(preferred_romantic_gender_display_text_list), text_color=CommonLocalizedStringColor.GREEN)
        else:
            preferred_romantic_gender_display_text = CommonLocalizationUtils.colorize(CommonStringId.S4CL_NONE, text_color=CommonLocalizedStringColor.GREEN)

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    CommonStringId.THIS_SIM_IS_ROMANTICALLY_ATTRACTED_TO,
                    preferred_romantic_gender_display_text,
                    icon=CommonIconUtils.load_arrow_right_icon()
                ),
                on_chosen=lambda *_, **__: self._modify_sexual_orientation(GenderPreferenceType.ROMANTIC, CommonStringId.THIS_SIM_IS_ROMANTICALLY_ATTRACTED_TO, preferred_romantic_gender_display_text, on_close=reopen)
            )
        )

        preferred_woohoo_genders = CommonSimGenderPreferenceUtils.determine_preferred_genders(self._sim_info, preference_type=GenderPreferenceType.WOOHOO)

        if preferred_woohoo_genders:
            preferred_woohoo_gender_display_text_list = [CommonGender.convert_to_localized_string_id(gender) for gender in preferred_woohoo_genders]
            preferred_woohoo_gender_display_text = CommonLocalizationUtils.colorize(CommonLocalizationUtils.combine_localized_strings_with_comma_space_and(preferred_woohoo_gender_display_text_list), text_color=CommonLocalizedStringColor.GREEN)
        else:
            preferred_woohoo_gender_display_text = CommonLocalizationUtils.colorize(CommonStringId.S4CL_NONE, text_color=CommonLocalizedStringColor.GREEN)

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    CommonStringId.THIS_SIM_IS_INTERESTED_IN_WOOHOO_WITH,
                    preferred_woohoo_gender_display_text,
                    icon=CommonIconUtils.load_arrow_right_icon()
                ),
                on_chosen=lambda *_, **__: self._modify_sexual_orientation(GenderPreferenceType.WOOHOO, CommonStringId.THIS_SIM_IS_INTERESTED_IN_WOOHOO_WITH, preferred_woohoo_gender_display_text, on_close=reopen)
            )
        )

    def _modify_sexual_orientation(self, preference_type: GenderPreferenceType, title: Union[int, CommonStringId, LocalizedString], description: Union[int, CommonStringId, LocalizedString], on_close: Callable[[], None]) -> None:
        def _on_close() -> None:
            on_close()

        option_dialog = CommonChooseObjectsOptionDialog(
            title,
            description,
            mod_identity=self.mod_identity,
            on_close=_on_close
        )

        def _on_submit(_chosen_genders: Tuple[CommonGender]):
            if _chosen_genders is None:
                _on_close()
                return
            for _chosen_gender in CommonGender.get_all():
                if _chosen_gender in _chosen_genders:
                    CommonSimGenderPreferenceUtils.set_preference_for_gender(self._sim_info, _chosen_gender, True, preference_type=preference_type)
                else:
                    CommonSimGenderPreferenceUtils.set_preference_for_gender(self._sim_info, _chosen_gender, False, preference_type=preference_type)
            _on_close()

        current_preferred_genders = CommonSimGenderPreferenceUtils.determine_preferred_genders(self._sim_info, preference_type=preference_type)

        for gender in CommonGender.get_all():
            icon = CommonIconUtils.load_unfilled_circle_icon()
            is_selected = gender in current_preferred_genders
            if is_selected:
                icon = CommonIconUtils.load_checked_circle_icon()
            option_dialog.add_option(
                CommonDialogSelectOption(
                    gender.name,
                    gender,
                    CommonDialogOptionContext(
                        CommonGender.convert_to_localized_string_id(gender),
                        0,
                        icon=icon,
                        is_selected=is_selected
                    )
                )
            )

        option_dialog.show(
            sim_info=self._sim_info,
            on_submit=_on_submit,
            min_selectable=0,
            max_selectable=option_dialog.option_count
        )

    def _pregnancy_options(self, on_close: Callable[[], None] = None) -> None:
        def _on_close() -> None:
            if on_close is not None:
                on_close()

        def _reopen() -> None:
            self._pregnancy_options(on_close=on_close)

        option_dialog = CommonChooseObjectOptionDialog(
            CGSStringId.CGS_PREGNANCY_OPTIONS_NAME,
            CGSStringId.CGS_PREGNANCY_OPTIONS_DESCRIPTION,
            mod_identity=self.mod_identity,
            on_close=_on_close
        )

        if CommonSpeciesUtils.is_animal(self._sim_info):
            def _on_reproductive_chosen(_: str, picked_option: bool):
                if picked_option is None:
                    _on_close()
                    return
                value = not CommonSimGenderOptionUtils.can_reproduce(self._sim_info)
                CommonSimGenderOptionUtils.update_can_reproduce(self._sim_info, value)
                _reopen()

            current_selected_text = CGSStringId.NATURAL
            can_reproduce = CommonSimGenderOptionUtils.can_reproduce(self._sim_info)
            if not can_reproduce:
                current_selected_text = CGSStringId.FIXED

            option_dialog.add_option(
                CommonDialogToggleOption(
                    'Reproductive Settings',
                    can_reproduce,
                    CommonDialogOptionContext(
                        CGSStringId.REPRODUCTIVE_SETTINGS,
                        CommonLocalizationUtils.colorize(current_selected_text, text_color=CommonLocalizedStringColor.GREEN),
                        icon=CommonIconUtils.load_question_mark_icon()
                    ),
                    on_chosen=_on_reproductive_chosen
                )
            )

        def _can_impregnate_chosen(option_identifier: str, can_get_others_pregnant: bool):
            self.log.format(option_identifier=option_identifier, can_get_others_pregnant=can_get_others_pregnant)
            value = not CommonSimGenderOptionUtils.can_impregnate(self._sim_info)
            CommonSimGenderOptionUtils.update_can_impregnate(self._sim_info, value)
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

    def _set_voice_actor(self, on_close: Callable[[], None] = None) -> None:
        def _on_close() -> None:
            if on_close is not None:
                on_close()

        voice_actor = CommonSimVoiceUtils.get_voice_actor(self._sim_info)
        option_dialog = CommonChooseObjectOptionDialog(
            CGSStringId.SET_VOICE_ACTOR_TITLE,
            CGSStringId.SET_VOICE_ACTOR_DESCRIPTION,
            title_tokens=(
                str(voice_actor.name if isinstance(voice_actor, CommonVoiceActorType) else voice_actor),
            ),
            mod_identity=self.mod_identity,
            on_close=_on_close
        )

        @CommonExceptionHandler.catch_exceptions(self.mod_identity, fallback_return=False)
        def _on_chosen(_: str, chosen: CommonVoiceActorType) -> None:
            if chosen is None:
                self.log.format_with_message('No chosen', chosen=chosen)
                _on_close()
                return
            CommonSimVoiceUtils.set_voice_actor(self._sim_info, chosen)
            _on_close()

        voice_actor_types = CommonSimVoiceUtils.determine_available_voice_types(self._sim_info)
        for voice_actor_type in voice_actor_types:
            option_dialog.add_option(
                CommonDialogSelectOption(
                    voice_actor_type.name,
                    voice_actor_type,
                    CommonDialogOptionContext(
                        voice_actor_type.name,
                        0,
                        icon=CommonIconUtils.load_checked_square_icon() if voice_actor_type == voice_actor else CommonIconUtils.load_unchecked_square_icon()
                    ),
                    on_chosen=_on_chosen
                )
            )

        option_dialog.show(sim_info=self._sim_info)
