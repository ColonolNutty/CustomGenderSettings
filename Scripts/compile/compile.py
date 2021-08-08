"""
This file is part of the Custom Gender Settings mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from Utilities.unpyc3_compiler import Unpyc3PythonCompiler


release_dir = os.path.join('..', '..', 'Release', 'CustomGenderSettings')

Unpyc3PythonCompiler.compile_mod(
    folder_path_to_output_ts4script_to=release_dir,
    names_of_modules_include=('customgendersettings',),
    output_ts4script_name='customgendersettings'
)
