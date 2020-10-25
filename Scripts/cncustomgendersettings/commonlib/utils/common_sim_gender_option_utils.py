"""
This file is part of the Custom Gender Settings mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils


class CGSCommonSimGenderOptionUtils:
    """ Utils for gender options of SIms. """
    @staticmethod
    def has_breasts(sim_info: SimInfo) -> bool:
        """has_breasts(sim_info)

        Determine if a Sim has breasts.

        .. note:: This will True if breasts are being forced on the Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has breasts. False, if not.
        :rtype: bool
        """
        if CommonGenderUtils.is_female(sim_info) and not CommonTraitUtils.has_trait(sim_info, CommonTraitId.BREASTS_FORCE_OFF):
            return True
        if CommonGenderUtils.is_male(sim_info) and CommonTraitUtils.has_trait(sim_info, CommonTraitId.BREASTS_FORCE_ON):
            return True
        return False

    @staticmethod
    def update_has_breasts(sim_info: SimInfo, has_breasts: bool) -> bool:
        """update_has_breasts(sim_info, has_breasts)

        Give or Take Away the breasts of a Sim.

        .. note:: Will only update Human Sims.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param has_breasts: If True, the Sim will be given breasts.\
        If False, the Sim will not longer have breasts.
        :type has_breasts: bool
        :return: True, if the state of a Sim having breasts or not was changed. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            return False
        CommonTraitUtils.remove_trait(sim_info, CommonTraitId.BREASTS_FORCE_OFF)
        CommonTraitUtils.remove_trait(sim_info, CommonTraitId.BREASTS_FORCE_ON)
        if has_breasts:
            if CommonGenderUtils.is_male(sim_info):
                CommonTraitUtils.add_trait(sim_info, CommonTraitId.BREASTS_FORCE_ON)
                CommonOutfitUtils.update_outfits(sim_info)
                return True
        else:
            if CommonGenderUtils.is_female(sim_info):
                CommonTraitUtils.add_trait(sim_info, CommonTraitId.BREASTS_FORCE_OFF)
                CommonOutfitUtils.update_outfits(sim_info)
                return True
        return False
