"""
This file is part of the Custom Gender Settings mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""

from typing import Type, Union, Dict, Any

from customgendersettings.modinfo import ModInfo
from customgendersettings.persistence.cgs_data_manager import CGSDataManager
from customgendersettings.settings.data.data_store import CGSGlobalSettingsDataStore
from sims4communitylib.persistence.data_management.common_data_manager_registry import CommonDataManagerRegistry
from sims4communitylib.persistence.data_stores.common_data_store import CommonDataStore
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4.commands import Command, CommandType, CheatOutput


class CGSDataManagerUtils(CommonService):
    """ Utilities for accessing data stores """
    def __init__(self) -> None:
        self._data_manager: CGSDataManager = None

    @property
    def data_manager(self) -> CGSDataManager:
        """ The data manager containing data. """
        if self._data_manager is None:
            self._data_manager: CGSDataManager = CommonDataManagerRegistry().locate_data_manager(ModInfo.get_identity())
        return self._data_manager

    def get_global_mod_settings_data_store(self) -> CGSGlobalSettingsDataStore:
        """ Retrieve the Global Mod Settings Data Store. """
        data_store: CGSGlobalSettingsDataStore = self._get_data_store(CGSGlobalSettingsDataStore)
        return data_store

    def _get_data_store(self, data_store_type: Type[CommonDataStore]) -> Union[CommonDataStore, None]:
        return self.data_manager.get_data_store_by_type(data_store_type)

    def get_all_data(self) -> Dict[str, Dict[str, Any]]:
        """ Get all data. """
        return self.data_manager._data_store_data

    def save(self) -> bool:
        """ Save data. """
        return self.data_manager.save()

    def reset(self, prevent_save: bool=False) -> bool:
        """ Reset data. """
        return self.data_manager.remove_all_data(prevent_save=prevent_save)


log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'cgs.print_mod_data')


@Command('cgs.print_mod_data', command_type=CommandType.Live)
def _cgs_command_print_mod_data(_connection: int=None):
    output = CheatOutput(_connection)
    output('Printing CGS Mod Data to Messages.txt file. This may take a little bit, be patient.')
    log.enable()
    log.format(data_store_data=CGSDataManagerUtils().get_all_data())
    log.disable()
    output('Done')


@Command('cgs.clear_mod_data', command_type=CommandType.Live)
def _cgs_command_clear_global_settings(_connection: int=None):
    output = CheatOutput(_connection)
    output('Clearing CGS Mod Data.')
    CGSDataManagerUtils().reset(prevent_save=True)
    output('!!! PLEASE READ !!!')
    output('Settings reset to default. Please restart your game without saving.')
    output('!!!!!!!!!!!!!!!!!!!')
