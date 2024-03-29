"""
Custom Gender Settings is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from customgendersettings.modinfo import ModInfo
from sims.sim_info_types import Species
from sims4.resources import Types
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_early_load import S4CLZoneEarlyLoadEvent
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from traits.traits import Trait


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _cgs_update_traits_on_zone_early_load(event_data: S4CLZoneEarlyLoadEvent):
    if event_data.game_loaded:
        # If the game is loaded already, it means we have already done this.
        return True
    # noinspection PyTypeChecker
    toilet_standing_trait: Trait = CommonResourceUtils.load_instance(Types.TRAIT, CommonTraitId.GENDER_OPTIONS_TOILET_STANDING)
    toilet_standing_trait.conflicting_traits = tuple()

    # noinspection PyTypeChecker
    toilet_sitting_trait: Trait = CommonResourceUtils.load_instance(Types.TRAIT, CommonTraitId.GENDER_OPTIONS_TOILET_SITTING)
    toilet_sitting_trait.conflicting_traits = tuple()

    # noinspection PyTypeChecker
    can_reproduce_trait: Trait = CommonResourceUtils.load_instance(Types.TRAIT, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_REPRODUCE)
    can_reproduce_trait.species = tuple(can_reproduce_trait.species) + (Species.FOX,)

    # noinspection PyTypeChecker
    cannot_reproduce_trait: Trait = CommonResourceUtils.load_instance(Types.TRAIT, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_NOT_REPRODUCE)
    cannot_reproduce_trait.species = tuple(cannot_reproduce_trait.species) + (Species.FOX,)
