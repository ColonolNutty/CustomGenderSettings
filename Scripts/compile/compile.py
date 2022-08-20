"""
Custom Gender Settings is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from Utilities.unpyc3_compiler import Unpyc3PythonCompiler


release_dir = os.path.join('..', '..', 'Release', 'CustomGenderSettings', 'Mods')

Unpyc3PythonCompiler.compile_mod(
    folder_path_to_output_ts4script_to=release_dir,
    names_of_modules_include=('customgendersettings',),
    output_ts4script_name='customgendersettings'
)
