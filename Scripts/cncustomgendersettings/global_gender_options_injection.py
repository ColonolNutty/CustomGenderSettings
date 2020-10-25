"""
This file is part of the Custom Gender Settings mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from cncustomgendersettings.commonlib.utils.common_sim_gender_option_utils import CGSCommonSimGenderOptionUtils
from cncustomgendersettings.modinfo import ModInfo
from cncustomgendersettings.persistence.cgs_sim_data import CGSSimData
from cncustomgendersettings.settings.setting_utils import CGSSettingUtils
from sims.occult.occult_enums import OccultType
from sims.outfits.outfit_utils import get_maximum_outfits_for_category
from sims.sim_info import SimInfo
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.sim.events.sim_spawned import S4CLSimSpawnedEvent
from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils


class _CGSUpdateGenderOptions:
    def __init__(self) -> None:
        self._setting_utils = CGSSettingUtils()

    def _update_gender_options(self, sim_info: SimInfo):
        CGSSimData(sim_info).update_original_gender_options()
        update_outfits = False
        if self._setting_utils.force_all_sims_to_male() and not CommonGenderUtils.is_male(sim_info):
            CommonGenderUtils.swap_gender(sim_info)
            update_outfits = True
        elif self._setting_utils.force_all_sims_to_female() and not CommonGenderUtils.is_female(sim_info):
            CommonGenderUtils.swap_gender(sim_info)
            update_outfits = True
        if CommonGenderUtils.is_male(sim_info):
            if CommonSpeciesUtils.is_pet(sim_info):
                if self._setting_utils.all_male_options.can_reproduce() and not CommonSimGenderOptionUtils.can_reproduce(sim_info):
                    CommonSimGenderOptionUtils.update_can_reproduce(sim_info, True)
                if self._setting_utils.all_male_options.cannot_reproduce() and not CommonSimGenderOptionUtils.can_not_reproduce(sim_info):
                    CommonSimGenderOptionUtils.update_can_reproduce(sim_info, False)
            elif CommonSpeciesUtils.is_human(sim_info):
                if self._setting_utils.all_male_options.use_toilet_standing() and not CommonSimGenderOptionUtils.uses_toilet_standing(sim_info):
                    CommonSimGenderOptionUtils.update_toilet_usage(sim_info, True)
                    update_outfits = True
                if self._setting_utils.all_male_options.use_toilet_sitting() and not CommonSimGenderOptionUtils.uses_toilet_sitting(sim_info):
                    CommonSimGenderOptionUtils.update_toilet_usage(sim_info, False)
                    update_outfits = True
                if self._setting_utils.all_male_options.prefer_menswear() and not CommonSimGenderOptionUtils.prefers_menswear(sim_info):
                    CommonSimGenderOptionUtils.update_clothing_preference(sim_info, True)
                if self._setting_utils.all_male_options.prefer_womenswear() and not CommonSimGenderOptionUtils.prefers_womenswear(sim_info):
                    CommonSimGenderOptionUtils.update_clothing_preference(sim_info, False)
                if self._setting_utils.all_male_options.force_masculine_body_frame() and not CommonSimGenderOptionUtils.has_masculine_frame(sim_info):
                    CommonSimGenderOptionUtils.update_body_frame(sim_info, True)
                if self._setting_utils.all_male_options.force_feminine_body_frame() and not CommonSimGenderOptionUtils.has_feminine_frame(sim_info):
                    CommonSimGenderOptionUtils.update_body_frame(sim_info, False)
                if self._setting_utils.all_male_options.can_impregnate() and not CommonSimGenderOptionUtils.can_impregnate(sim_info):
                    CommonSimGenderOptionUtils.update_can_impregnate(sim_info, True)
                if self._setting_utils.all_male_options.cannot_impregnate() and not CommonSimGenderOptionUtils.can_not_impregnate(sim_info):
                    CommonSimGenderOptionUtils.update_can_impregnate(sim_info, False)
                if self._setting_utils.all_male_options.can_be_impregnated() and not CommonSimGenderOptionUtils.can_be_impregnated(sim_info):
                    CommonSimGenderOptionUtils.update_can_be_impregnated(sim_info, True)
                if self._setting_utils.all_male_options.cannot_be_impregnated() and not CommonSimGenderOptionUtils.can_not_be_impregnated(sim_info):
                    CommonSimGenderOptionUtils.update_can_be_impregnated(sim_info, False)
                if self._setting_utils.all_male_options.force_breasts_on() and not CGSCommonSimGenderOptionUtils.has_breasts(sim_info):
                    CGSCommonSimGenderOptionUtils.update_has_breasts(sim_info, True)
                    update_outfits = True
                if self._setting_utils.all_male_options.force_breasts_off() and CGSCommonSimGenderOptionUtils.has_breasts(sim_info):
                    CGSCommonSimGenderOptionUtils.update_has_breasts(sim_info, False)
                    update_outfits = True
        elif CommonGenderUtils.is_female(sim_info):
            if CommonSpeciesUtils.is_pet(sim_info):
                if self._setting_utils.all_female_options.can_reproduce() and not CommonSimGenderOptionUtils.can_reproduce(sim_info):
                    CommonSimGenderOptionUtils.update_can_reproduce(sim_info, True)
                if self._setting_utils.all_female_options.cannot_reproduce() and not CommonSimGenderOptionUtils.can_not_reproduce(sim_info):
                    CommonSimGenderOptionUtils.update_can_reproduce(sim_info, False)
            elif CommonSpeciesUtils.is_human(sim_info):
                if self._setting_utils.all_female_options.use_toilet_standing() and not CommonSimGenderOptionUtils.uses_toilet_standing(sim_info):
                    CommonSimGenderOptionUtils.update_toilet_usage(sim_info, True)
                    update_outfits = True
                if self._setting_utils.all_female_options.use_toilet_sitting() and not CommonSimGenderOptionUtils.uses_toilet_sitting(sim_info):
                    CommonSimGenderOptionUtils.update_toilet_usage(sim_info, False)
                    update_outfits = True
                if self._setting_utils.all_female_options.prefer_menswear() and not CommonSimGenderOptionUtils.prefers_menswear(sim_info):
                    CommonSimGenderOptionUtils.update_clothing_preference(sim_info, True)
                if self._setting_utils.all_female_options.prefer_womenswear() and not CommonSimGenderOptionUtils.prefers_womenswear(sim_info):
                    CommonSimGenderOptionUtils.update_clothing_preference(sim_info, False)
                if self._setting_utils.all_female_options.force_masculine_body_frame() and not CommonSimGenderOptionUtils.has_masculine_frame(sim_info):
                    CommonSimGenderOptionUtils.update_body_frame(sim_info, True)
                if self._setting_utils.all_female_options.force_feminine_body_frame() and not CommonSimGenderOptionUtils.has_feminine_frame(sim_info):
                    CommonSimGenderOptionUtils.update_body_frame(sim_info, False)
                if self._setting_utils.all_female_options.can_impregnate() and not CommonSimGenderOptionUtils.can_impregnate(sim_info):
                    CommonSimGenderOptionUtils.update_can_impregnate(sim_info, True)
                if self._setting_utils.all_female_options.cannot_impregnate() and not CommonSimGenderOptionUtils.can_not_impregnate(sim_info):
                    CommonSimGenderOptionUtils.update_can_impregnate(sim_info, False)
                if self._setting_utils.all_female_options.can_be_impregnated() and not CommonSimGenderOptionUtils.can_be_impregnated(sim_info):
                    CommonSimGenderOptionUtils.update_can_be_impregnated(sim_info, True)
                if self._setting_utils.all_female_options.cannot_be_impregnated() and not CommonSimGenderOptionUtils.can_not_be_impregnated(sim_info):
                    CommonSimGenderOptionUtils.update_can_be_impregnated(sim_info, False)
                if self._setting_utils.all_female_options.force_breasts_on() and not CGSCommonSimGenderOptionUtils.has_breasts(sim_info):
                    CGSCommonSimGenderOptionUtils.update_has_breasts(sim_info, True)
                    update_outfits = True
                if self._setting_utils.all_female_options.force_breasts_off() and CGSCommonSimGenderOptionUtils.has_breasts(sim_info):
                    CGSCommonSimGenderOptionUtils.update_has_breasts(sim_info, False)
                    update_outfits = True
        if update_outfits:
            CommonOutfitUtils.update_outfits(sim_info)

    def _regenerate_every_outfit(self, sim_info: SimInfo) -> bool:
        result = False
        for occult_base_sim_info in CommonOccultUtils.get_sim_info_for_all_occults_gen(sim_info, (OccultType.MERMAID,)):
            for outfit_category in CommonOutfitUtils.get_all_outfit_categories():
                for outfit_index in range(get_maximum_outfits_for_category(outfit_category)):
                    if not CommonOutfitUtils.has_outfit(occult_base_sim_info, (outfit_category, outfit_index)):
                        continue

                    if CommonOutfitUtils.generate_outfit(occult_base_sim_info, outfit_category_and_index=(outfit_category, outfit_index)):
                        result = True

        if result:
            CommonOutfitUtils.update_outfits(sim_info)
        return result


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _cgs_apply_global_settings_on_sim_spawn(event_data: S4CLSimSpawnedEvent) -> bool:
    sim_info = event_data.sim_info
    _CGSUpdateGenderOptions()._update_gender_options(sim_info)
    return True
