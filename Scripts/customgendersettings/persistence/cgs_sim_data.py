"""
Custom Gender Settings is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat

from customgendersettings.modinfo import ModInfo
from sims4.commands import Command, CommandType, CheatOutput
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.persistence.common_persisted_sim_data_storage import CommonPersistedSimDataStorage
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


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


@Command('cgs.print_sim_data', command_type=CommandType.Live)
def _cgs_command_print_sim_data(_connection: int=None):
    output = CheatOutput(_connection)
    sim_info = CommonSimUtils.get_active_sim_info()
    output('Sim Data for Sim: Name: \'{}\' Id: \'{}\''.format(CommonSimNameUtils.get_full_name(sim_info), CommonSimUtils.get_sim_id(sim_info)))
    sim_storage = CGSSimData(sim_info)
    for (key, value) in sim_storage._data.items():
        output(' > {}: {}'.format(pformat(key), pformat(value)))
