# -*- coding: utf-8 -*-
""" Basic test for instantioation of the object and inital file checks """

from pathlib import Path

import pytest
from py_mal_dll.create_dll import DllCreator
from tests.utils import FAKE_DLL_NAME, FAKE_DLL_PATH, FAKE_FUNCTION_LIST_1


def test_create_class_basic(output_folder):
    creator = DllCreator(original_dll="test", outfolder=output_folder)
    assert Path(output_folder).exists() is True
    assert creator.outfolder == output_folder


def test_create_class_output_already_exist(created_output_folder):
    with pytest.raises(FileExistsError):
        DllCreator._create_output_folder(folder_name=created_output_folder)


def test_created_params(dll_creator_fake_taget):
    assert dll_creator_fake_taget.original_dll_name == FAKE_DLL_NAME
    assert dll_creator_fake_taget.original_dll_path == FAKE_DLL_PATH
    assert dll_creator_fake_taget.parsed["exports"] is False
    assert dll_creator_fake_taget.parsed["version"] is False


def test_create_parse_exports(dll_creator_mocked_pefile):
    expected_funclist = set(zip(range(len(FAKE_FUNCTION_LIST_1)), FAKE_FUNCTION_LIST_1))
    dll_creator_mocked_pefile.parse_exports()
    assert dll_creator_mocked_pefile.parsed["exports"] is True
    assert dll_creator_fake_taget.parsed["version"] is False
    assert (
        set(dll_creator_mocked_pefile.target_dll_exported_functions)
        == expected_funclist
    )


def test_parse_version_info():
    pass
