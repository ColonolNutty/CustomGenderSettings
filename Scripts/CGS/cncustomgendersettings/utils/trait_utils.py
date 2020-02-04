"""
This file is part of the Custom Gender Settings mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils


class CGSTraitUtils:
    """ Trait Utilities used by the CGS mod. """
    @classmethod
    def flip_traits(cls, sim_info: SimInfo, trait_one: int, trait_two: int) -> bool:
        """ Flip two traits, adding one while removing the other. """
        # Has Trait One
        if CommonTraitUtils.has_trait(sim_info, trait_one):
            CommonTraitUtils.remove_trait(sim_info, trait_one)
            if not CommonTraitUtils.has_trait(sim_info, trait_two):
                CommonTraitUtils.add_trait(sim_info, trait_two)
            return True
        # Has Trait Two
        elif CommonTraitUtils.has_trait(sim_info, trait_two):
            CommonTraitUtils.remove_trait(sim_info, trait_two)
            if not CommonTraitUtils.has_trait(sim_info, trait_one):
                CommonTraitUtils.add_trait(sim_info, trait_one)
            return True
        return False
