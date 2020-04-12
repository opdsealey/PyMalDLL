# -*- coding: utf-8 -*-
""" global pytest configuration """
from pathlib import Path

import py_mal_dll.create_dll
import pytest
from tests.utils import FAKE_DLL_PATH, TEST_OUTPUT_FOLDER_NAME, mocked_pefile

""" Basic cleanup if any folders stll exist """


@pytest.fixture
def base_dir(tmp_path_factory):
    path = tmp_path_factory.mktemp(TEST_OUTPUT_FOLDER_NAME)
    return path


@pytest.fixture
def created_output_folder(base_dir):
    path = Path(base_dir) / "created_output_folder"
    path.mkdir()
    yield path


@pytest.fixture
def output_folder(base_dir):
    path = Path(base_dir) / "output_folder"
    yield path


@pytest.fixture
def dll_creator_fake_taget(output_folder):
    creator = py_mal_dll.create_dll.DllCreator(
        original_dll=FAKE_DLL_PATH, outfolder=output_folder
    )
    return creator


@pytest.fixture
def dll_creator_mocked_pefile(output_folder):
    py_mal_dll.create_dll.pefile = mocked_pefile
    creator = py_mal_dll.create_dll.DllCreator(
        original_dll=FAKE_DLL_PATH, outfolder=output_folder
    )
    return creator
