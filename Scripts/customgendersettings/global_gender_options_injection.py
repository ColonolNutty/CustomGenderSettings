"""
Custom Gender Settings is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from customgendersettings.modinfo import ModInfo
from customgendersettings.settings.setting_utils import CGSSettingUtils
from sims.sim_info import SimInfo
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.sim.events.sim_spawned import S4CLSimSpawnedEvent
from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils


class _CGSUpdateGenderOptions:
    def __init__(self) -> None:
        self._setting_utils = CGSSettingUtils()

    def _apply_global_updates(self, sim_info: SimInfo):
        update_outfits = False
        if self._setting_utils.force_all_sims_to_male() and not CommonGenderUtils.is_male(sim_info):
            CommonGenderUtils.swap_gender(sim_info, update_outfits=False)
            update_outfits = True
        elif self._setting_utils.force_all_sims_to_female() and not CommonGenderUtils.is_female(sim_info):
            CommonGenderUtils.swap_gender(sim_info, update_outfits=False)
            update_outfits = True

        if CommonGenderUtils.is_male(sim_info):
            if self._setting_utils.all_male_options.use_toilet_standing() and not CommonSimGenderOptionUtils.uses_toilet_standing(sim_info):
                CommonSimGenderOptionUtils.set_can_use_toilet_standing(sim_info, True)
                update_outfits = True
            if self._setting_utils.all_male_options.dont_use_toilet_standing() and CommonSimGenderOptionUtils.uses_toilet_standing(sim_info):
                CommonSimGenderOptionUtils.set_can_use_toilet_standing(sim_info, False)
                update_outfits = True
            if self._setting_utils.all_male_options.use_toilet_sitting() and not CommonSimGenderOptionUtils.uses_toilet_sitting(sim_info):
                CommonSimGenderOptionUtils.set_can_use_toilet_sitting(sim_info, True)
                update_outfits = True
            if self._setting_utils.all_male_options.dont_use_toilet_sitting() and CommonSimGenderOptionUtils.uses_toilet_sitting(sim_info):
                CommonSimGenderOptionUtils.set_can_use_toilet_sitting(sim_info, False)
                update_outfits = True
            if self._setting_utils.all_male_options.can_impregnate() and not CommonSimGenderOptionUtils.can_impregnate(sim_info):
                CommonSimGenderOptionUtils.update_can_impregnate(sim_info, True)
            if self._setting_utils.all_male_options.cannot_impregnate() and not CommonSimGenderOptionUtils.can_not_impregnate(sim_info):
                CommonSimGenderOptionUtils.update_can_impregnate(sim_info, False)
            if self._setting_utils.all_male_options.can_be_impregnated() and not CommonSimGenderOptionUtils.can_be_impregnated(sim_info):
                CommonSimGenderOptionUtils.update_can_be_impregnated(sim_info, True)
            if self._setting_utils.all_male_options.cannot_be_impregnated() and not CommonSimGenderOptionUtils.can_not_be_impregnated(sim_info):
                CommonSimGenderOptionUtils.update_can_be_impregnated(sim_info, False)

            if CommonSpeciesUtils.is_animal(sim_info):
                if self._setting_utils.all_male_options.can_reproduce() and not CommonSimGenderOptionUtils.can_reproduce(sim_info):
                    CommonSimGenderOptionUtils.update_can_reproduce(sim_info, True)
                if self._setting_utils.all_male_options.cannot_reproduce() and not CommonSimGenderOptionUtils.can_not_reproduce(sim_info):
                    CommonSimGenderOptionUtils.update_can_reproduce(sim_info, False)
            elif CommonSpeciesUtils.is_human(sim_info):
                if self._setting_utils.all_male_options.prefer_menswear() and not CommonSimGenderOptionUtils.prefers_menswear(sim_info):
                    CommonSimGenderOptionUtils.update_clothing_preference(sim_info, True)
                if self._setting_utils.all_male_options.prefer_womenswear() and not CommonSimGenderOptionUtils.prefers_womenswear(sim_info):
                    CommonSimGenderOptionUtils.update_clothing_preference(sim_info, False)
                if self._setting_utils.all_male_options.force_masculine_body_frame() and not CommonSimGenderOptionUtils.has_masculine_frame(sim_info):
                    CommonSimGenderOptionUtils.update_body_frame(sim_info, True)
                if self._setting_utils.all_male_options.force_feminine_body_frame() and not CommonSimGenderOptionUtils.has_feminine_frame(sim_info):
                    CommonSimGenderOptionUtils.update_body_frame(sim_info, False)
                if self._setting_utils.all_male_options.force_breasts_on() and not CommonSimGenderOptionUtils.has_breasts(sim_info):
                    CommonSimGenderOptionUtils.update_has_breasts(sim_info, True)
                    update_outfits = True
                if self._setting_utils.all_male_options.force_breasts_off() and CommonSimGenderOptionUtils.has_breasts(sim_info):
                    CommonSimGenderOptionUtils.update_has_breasts(sim_info, False)
                    update_outfits = True
        elif CommonGenderUtils.is_female(sim_info):
            if self._setting_utils.all_female_options.use_toilet_standing() and not CommonSimGenderOptionUtils.uses_toilet_standing(sim_info):
                CommonSimGenderOptionUtils.set_can_use_toilet_standing(sim_info, True)
                update_outfits = True
            if self._setting_utils.all_female_options.dont_use_toilet_standing() and CommonSimGenderOptionUtils.uses_toilet_standing(sim_info):
                CommonSimGenderOptionUtils.set_can_use_toilet_standing(sim_info, False)
                update_outfits = True
            if self._setting_utils.all_female_options.use_toilet_sitting() and not CommonSimGenderOptionUtils.uses_toilet_sitting(sim_info):
                CommonSimGenderOptionUtils.set_can_use_toilet_sitting(sim_info, True)
                update_outfits = True
            if self._setting_utils.all_female_options.dont_use_toilet_sitting() and CommonSimGenderOptionUtils.uses_toilet_sitting(sim_info):
                CommonSimGenderOptionUtils.set_can_use_toilet_sitting(sim_info, False)
                update_outfits = True
            if self._setting_utils.all_female_options.can_impregnate() and not CommonSimGenderOptionUtils.can_impregnate(sim_info):
                CommonSimGenderOptionUtils.update_can_impregnate(sim_info, True)
            if self._setting_utils.all_female_options.cannot_impregnate() and not CommonSimGenderOptionUtils.can_not_impregnate(sim_info):
                CommonSimGenderOptionUtils.update_can_impregnate(sim_info, False)
            if self._setting_utils.all_female_options.can_be_impregnated() and not CommonSimGenderOptionUtils.can_be_impregnated(sim_info):
                CommonSimGenderOptionUtils.update_can_be_impregnated(sim_info, True)
            if self._setting_utils.all_female_options.cannot_be_impregnated() and not CommonSimGenderOptionUtils.can_not_be_impregnated(sim_info):
                CommonSimGenderOptionUtils.update_can_be_impregnated(sim_info, False)

            if CommonSpeciesUtils.is_animal(sim_info):
                if self._setting_utils.all_female_options.can_reproduce() and not CommonSimGenderOptionUtils.can_reproduce(sim_info):
                    CommonSimGenderOptionUtils.update_can_reproduce(sim_info, True)
                if self._setting_utils.all_female_options.cannot_reproduce() and not CommonSimGenderOptionUtils.can_not_reproduce(sim_info):
                    CommonSimGenderOptionUtils.update_can_reproduce(sim_info, False)
            elif CommonSpeciesUtils.is_human(sim_info):
                if self._setting_utils.all_female_options.prefer_menswear() and not CommonSimGenderOptionUtils.prefers_menswear(sim_info):
                    CommonSimGenderOptionUtils.update_clothing_preference(sim_info, True)
                if self._setting_utils.all_female_options.prefer_womenswear() and not CommonSimGenderOptionUtils.prefers_womenswear(sim_info):
                    CommonSimGenderOptionUtils.update_clothing_preference(sim_info, False)
                if self._setting_utils.all_female_options.force_masculine_body_frame() and not CommonSimGenderOptionUtils.has_masculine_frame(sim_info):
                    CommonSimGenderOptionUtils.update_body_frame(sim_info, True)
                if self._setting_utils.all_female_options.force_feminine_body_frame() and not CommonSimGenderOptionUtils.has_feminine_frame(sim_info):
                    CommonSimGenderOptionUtils.update_body_frame(sim_info, False)
                if self._setting_utils.all_female_options.force_breasts_on() and not CommonSimGenderOptionUtils.has_breasts(sim_info):
                    CommonSimGenderOptionUtils.update_has_breasts(sim_info, True)
                    update_outfits = True
                if self._setting_utils.all_female_options.force_breasts_off() and CommonSimGenderOptionUtils.has_breasts(sim_info):
                    CommonSimGenderOptionUtils.update_has_breasts(sim_info, False)
                    update_outfits = True
        if update_outfits:
            CommonOutfitUtils.update_outfits(sim_info)
            CommonOutfitUtils.regenerate_all_outfits(sim_info)


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _cgs_apply_global_settings_on_sim_spawn(event_data: S4CLSimSpawnedEvent) -> bool:
    sim_info = event_data.sim_info
    _CGSUpdateGenderOptions()._apply_global_updates(sim_info)
    return True
