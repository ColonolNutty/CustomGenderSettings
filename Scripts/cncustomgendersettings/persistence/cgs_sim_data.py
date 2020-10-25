"""
This file is part of the Custom Gender Settings mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat

from cncustomgendersettings.commonlib.utils.common_sim_gender_option_utils import CGSCommonSimGenderOptionUtils
from cncustomgendersettings.modinfo import ModInfo
from sims.sim_info_types import Gender
from sims4.commands import Command, CommandType, CheatOutput
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.persistence.common_persisted_sim_data_storage import CommonPersistedSimDataStorage
from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils


class CGSSimData(CommonPersistedSimDataStorage):
    """ Sim data storage """
    # noinspection PyMissingOrEmptyDocstring,PyMethodParameters
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cgs_sim_data'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def original_gender(self) -> Gender:
        return self.get_data(default=None)

    @original_gender.setter
    def original_gender(self, value: Gender):
        self.set_data(value)

    # noinspection PyMissingOrEmptyDocstring
    @property
    def original_uses_toilet_standing(self) -> bool:
        return self.get_data(default=None)

    @original_uses_toilet_standing.setter
    def original_uses_toilet_standing(self, value: bool):
        self.set_data(value)

    # noinspection PyMissingOrEmptyDocstring
    @property
    def original_prefers_menswear(self) -> bool:
        return self.get_data(default=None)

    @original_prefers_menswear.setter
    def original_prefers_menswear(self, value: bool):
        self.set_data(value)

    # noinspection PyMissingOrEmptyDocstring
    @property
    def original_has_masculine_frame(self) -> bool:
        return self.get_data(default=None)

    @original_has_masculine_frame.setter
    def original_has_masculine_frame(self, value: bool):
        self.set_data(value)

    # noinspection PyMissingOrEmptyDocstring
    @property
    def original_can_reproduce(self) -> bool:
        return self.get_data(default=None)

    @original_can_reproduce.setter
    def original_can_reproduce(self, value: bool):
        self.set_data(value)

    # noinspection PyMissingOrEmptyDocstring
    @property
    def original_can_impregnate(self) -> bool:
        return self.get_data(default=None)

    @original_can_impregnate.setter
    def original_can_impregnate(self, value: bool):
        self.set_data(value)

    # noinspection PyMissingOrEmptyDocstring
    @property
    def original_can_be_impregnated(self) -> bool:
        return self.get_data(default=None)

    @original_can_be_impregnated.setter
    def original_can_be_impregnated(self, value: bool):
        self.set_data(value)

    # noinspection PyMissingOrEmptyDocstring
    @property
    def original_has_breasts(self) -> bool:
        return self.get_data(default=None)

    @original_has_breasts.setter
    def original_has_breasts(self, value: bool):
        self.set_data(value)

    def update_original_gender_options(self, force: bool=False) -> None:
        """ Update original gender options only if they are not currently set. """
        # noinspection PyAttributeOutsideInit
        self.original_gender = CommonGenderUtils.get_gender(self.sim_info) if self.original_gender is None or force else self.original_gender
        # noinspection PyAttributeOutsideInit
        self.original_uses_toilet_standing = CommonSimGenderOptionUtils.uses_toilet_standing(self.sim_info) if self.original_uses_toilet_standing is None or force else self.original_uses_toilet_standing
        # noinspection PyAttributeOutsideInit
        self.original_prefers_menswear = CommonSimGenderOptionUtils.prefers_menswear(self.sim_info) if self.original_prefers_menswear is None or force else self.original_prefers_menswear
        # noinspection PyAttributeOutsideInit
        self.original_has_masculine_frame = CommonSimGenderOptionUtils.has_masculine_frame(self.sim_info) if self.original_has_masculine_frame is None or force else self.original_has_masculine_frame
        # noinspection PyAttributeOutsideInit
        self.original_can_reproduce = CommonSimGenderOptionUtils.can_reproduce(self.sim_info) if self.original_can_reproduce is None or force else self.original_can_reproduce
        # noinspection PyAttributeOutsideInit
        self.original_can_impregnate = CommonSimGenderOptionUtils.can_impregnate(self.sim_info) if self.original_can_impregnate is None or force else self.original_can_impregnate
        # noinspection PyAttributeOutsideInit
        self.original_can_be_impregnated = CommonSimGenderOptionUtils.can_be_impregnated(self.sim_info) if self.original_can_be_impregnated is None or force else self.original_can_be_impregnated
        # noinspection PyAttributeOutsideInit
        self.original_has_breasts = CGSCommonSimGenderOptionUtils.has_breasts(self.sim_info) if self.original_has_breasts is None or force else self.original_has_breasts

    def reset_to_original_gender_and_gender_options(self) -> None:
        """ Update the Sim to their saved original gender options. """
        CommonGenderUtils.set_gender(self.sim_info, self.original_gender)
        if CommonSpeciesUtils.is_pet(self.sim_info):
            CommonSimGenderOptionUtils.update_can_reproduce(self.sim_info, self.original_can_reproduce)
        else:
            CommonSimGenderOptionUtils.update_toilet_usage(self.sim_info, self.original_uses_toilet_standing)
            CommonSimGenderOptionUtils.update_clothing_preference(self.sim_info, self.original_prefers_menswear)
            CommonSimGenderOptionUtils.update_body_frame(self.sim_info, self.original_has_masculine_frame)
            CommonSimGenderOptionUtils.update_can_impregnate(self.sim_info, self.original_can_impregnate)
            CommonSimGenderOptionUtils.update_can_be_impregnated(self.sim_info, self.original_can_be_impregnated)
            CGSCommonSimGenderOptionUtils.update_has_breasts(self.sim_info, self.original_has_breasts)


@Command('cgs.print_sim_data', command_type=CommandType.Live)
def _cgs_command_print_sim_data(_connection: int=None):
    output = CheatOutput(_connection)
    sim_info = CommonSimUtils.get_active_sim_info()
    output('Sim Data for Sim: Name: \'{}\' Id: \'{}\''.format(CommonSimNameUtils.get_full_name(sim_info), CommonSimUtils.get_sim_id(sim_info)))
    sim_storage = CGSSimData(sim_info)
    for (key, value) in sim_storage._data.items():
        output(' > {}: {}'.format(pformat(key), pformat(value)))
