"""
This file is part of the Custom Gender Settings mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from cncustomgendersettings.modinfo import ModInfo
from cncustomgendersettings.settings.setting_utils import CGSSettingUtils
from sims.occult.occult_enums import OccultType
from sims.outfits.outfit_utils import get_maximum_outfits_for_category
from sims.sim_info import SimInfo
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.sim.events.sim_spawned import S4CLSimSpawnedEvent
from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils


class _CGSUpdateGenderOptions:
    def _update_gender_options(self, sim_info: SimInfo):
        if CGSSettingUtils().force_all_sims_to_male() and not CommonGenderUtils.is_male(sim_info):
            CommonGenderUtils.swap_gender(sim_info)
            CommonOutfitUtils.update_outfits(sim_info)
        elif CGSSettingUtils().force_all_sims_to_female() and not CommonGenderUtils.is_female(sim_info):
            CommonGenderUtils.swap_gender(sim_info)
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
