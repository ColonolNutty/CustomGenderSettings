"""
This file is part of the Custom Gender Settings mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from cncustomgendersettings.utils.cgs_setting_utils import CGSSettingUtils
from objects.script_object import ScriptObject
from sims.sim import Sim
from sims4communitylib.services.interactions.interaction_registration_service import CommonInteractionRegistry, \
    CommonInteractionType, CommonScriptObjectInteractionHandler
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from cncustomgendersettings.enums.interactions_enum import CGSInteractionId


@CommonInteractionRegistry.register_interaction_handler(CommonInteractionType.ON_SCRIPT_OBJECT_LOAD)
class _CGSRegisterInteractionHandler(CommonScriptObjectInteractionHandler):
    """ Register Custom Gender Setting interactions to appear on sims."""
    # noinspection PyMissingOrEmptyDocstring
    @property
    def interactions_to_add(self) -> Tuple[int]:
        interactions: Tuple[int] = (
            CGSInteractionId.CGS_OPEN_CUSTOM_GENDER_SETTINGS,
        )
        return interactions

    # noinspection PyMissingOrEmptyDocstring
    def should_add(self, script_object: ScriptObject, *args, **kwargs) -> bool:
        if not CommonTypeUtils.is_sim_instance(script_object):
            return False
        script_object: Sim = script_object
        sim_info = CommonSimUtils.get_sim_info(script_object)
        return CGSSettingUtils.is_enabled_for_custom_gender_setting_interactions(sim_info)
