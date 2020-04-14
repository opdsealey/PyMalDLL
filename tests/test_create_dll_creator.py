# -*- coding: utf-8 -*-
""" Basic test for instantioation of the object and inital file checks """
from pathlib import Path

import pefile
import pytest
from py_mal_dll.create_dll import DllCreator
from tests.utils import FAKE_DLL_NAME, FAKE_DLL_PATH, FAKE_FUNCTION_LIST_1, mocked_pe


def test_create_class_basic(output_folder):
    creator = DllCreator(original_dll="test", outfolder=output_folder)
    assert Path(output_folder).exists() is True
    assert creator.outfolder == output_folder


def test_create_class_output_already_exist(created_output_folder):
    with pytest.raises(FileExistsError):
        DllCreator._create_output_folder(folder_name=created_output_folder)


def test_created_params(dll_creator_fake_taget):
    assert dll_creator_fake_taget.original_dll_name == FAKE_DLL_NAME
    assert dll_creator_fake_taget.original_dll_path == Path(FAKE_DLL_PATH).absolute()
    assert dll_creator_fake_taget.parsed["exports"] is False
    assert dll_creator_fake_taget.parsed["version"] is False


def test_create_parse_exports(monkeypatch, dll_creator_fake_taget):
    def mocked_PE(*args, **kwargs):
        return mocked_pe()

    expected_funclist = set(zip(range(len(FAKE_FUNCTION_LIST_1)), FAKE_FUNCTION_LIST_1))

    monkeypatch.setattr(
        pefile, "DIRECTORY_ENTRY", {"IMAGE_DIRECTORY_ENTRY_EXPORT": "DATA_DIRECTORIES"}
    )

    monkeypatch.setattr(pefile, "PE", mocked_PE)

    dll_creator_fake_taget.parse_exports()
    assert dll_creator_fake_taget.parsed["exports"]
    assert not dll_creator_fake_taget.parsed["version"]
    assert (
        set(dll_creator_fake_taget.target_dll_exported_functions) == expected_funclist
    )


def test_incorrect_order_render(dll_creator_fake_taget):
    assert not dll_creator_fake_taget.parsed["exports"]
    assert not dll_creator_fake_taget.parsed["version"]

    with pytest.raises(ValueError):
        dll_creator_fake_taget.render()

    assert not dll_creator_fake_taget.parsed["exports"]
    assert not dll_creator_fake_taget.parsed["version"]

    dll_creator_fake_taget.parsed["exports"] = True
    with pytest.raises(ValueError):
        dll_creator_fake_taget.render()

    assert dll_creator_fake_taget.parsed["exports"]
    assert not dll_creator_fake_taget.parsed["version"]

    dll_creator_fake_taget.parsed["exports"] = False
    dll_creator_fake_taget.parsed["version"] = True

    with pytest.raises(ValueError):
        dll_creator_fake_taget.render()

    assert not dll_creator_fake_taget.parsed["exports"]
    assert dll_creator_fake_taget.parsed["version"]
