""" Various functions used in multiple tests """
from pathlib import Path


def check_output_files_exist(output_folder, no_resource=False):
    # Check no extra files have been created
    all_files = [p.name for p in Path(output_folder).glob("*")]
    assert "dllmain.c" in all_files
    assert "exports.def" in all_files
    assert "MaliciousDll.vcxproj" in all_files
    assert "MaliciousDll.vcxproj.filters" in all_files
    assert "MaliciousDll.vcxproj.user" in all_files

    if not no_resource:
        assert "resource.rc" in all_files
