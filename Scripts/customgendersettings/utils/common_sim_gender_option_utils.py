from sims.sim_info import SimInfo
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils


class CGSCommonSimGenderOptionUtils:
    """Utilities for Sim Gender Options"""
    @staticmethod
    def set_can_use_toilet_standing(sim_info: SimInfo, can_use_toilet_standing: bool) -> bool:
        """set_can_use_toilet_standing(sim_info, can_use_toilet_standing)

        Allow or Disallow a Sim to use the toilet while standing.

        .. note:: Will only update Human Sims.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param can_use_toilet_standing: If True, the Sim will be able to use toilets while standing. If False, the Sim will not be able to use toilets while standing.
        :type can_use_toilet_standing: bool
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            return False
        if not CommonSpeciesUtils.is_human(sim_info):
            return False
        if can_use_toilet_standing:
            CommonTraitUtils.add_trait(sim_info, CommonTraitId.GENDER_OPTIONS_TOILET_STANDING)
        else:
            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.GENDER_OPTIONS_TOILET_STANDING)
        from sims4communitylib.events.sim.common_sim_event_dispatcher import CommonSimEventDispatcherService
        CommonSimEventDispatcherService()._on_sim_change_gender_options_toilet_usage(sim_info)
        return True

    @staticmethod
    def set_can_use_toilet_sitting(sim_info: SimInfo, can_use_toilet_sitting: bool) -> bool:
        """set_can_use_toilet_sitting(sim_info, can_use_toilet_sitting)

        Allow or Disallow a Sim to use the toilet while sitting.

        .. note:: Will only update Human Sims.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param can_use_toilet_sitting: If True, the Sim will be able to use toilets while sitting. If False, the Sim will not be able to use toilets while sitting.
        :type can_use_toilet_sitting: bool
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            return False
        if not CommonSpeciesUtils.is_human(sim_info):
            return False
        if can_use_toilet_sitting:
            CommonTraitUtils.add_trait(sim_info, CommonTraitId.GENDER_OPTIONS_TOILET_SITTING)
        else:
            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.GENDER_OPTIONS_TOILET_SITTING)
        from sims4communitylib.events.sim.common_sim_event_dispatcher import CommonSimEventDispatcherService
        CommonSimEventDispatcherService()._on_sim_change_gender_options_toilet_usage(sim_info)
        return True
