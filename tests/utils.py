# -*- coding: utf-8 -*-
""" Various decalaration and helper functions for testing """
from pathlib import Path

TEST_OUTPUT_FOLDER_NAME = "TEST_OUTPUT_FOLDER"
FAKE_DLL_PATH = r"X:\Some\Fake\Path\test.dll"
FAKE_DLL_NAME = "test.dll"
FAKE_FUNCTION_LIST_1 = ["Function1", "Function2", "", "Function4"]
BASE_PATH = Path(__file__).parent


class mocked_pefile:
    DIRECTORY_ENTRY = {"IMAGE_DIRECTORY_ENTRY_EXPORT": True}

    @staticmethod
    def PE(*args, **kwargs):
        return mocked_pe()


class ExportData:
    def __init__(self, ordinal, name=""):
        self.ordinal = ordinal
        self.name = name


class mocked_pe:
    def __init__(self, *args, **kwargs):
        self.DIRECTORY_ENTRY_EXPORT = self._DIRECTORY_ENTRY_EXPORT()
        self.VS_FIXEDFILEINFO = [
            self.VS_FIXEDFILEINFO_entry(),
            self.VS_FIXEDFILEINFO_entry(),
        ]

        self.FileInfo = []

    @staticmethod
    def parse_data_directories(*args, **kwargs):
        return

    class _DIRECTORY_ENTRY_EXPORT:
        symbols = [ExportData(i, n) for i, n in enumerate(FAKE_FUNCTION_LIST_1)]

    class VS_FIXEDFILEINFO_entry:
        FileFlagsMask = 1
        FileFlags = 20
        FileOS = 0x1

    class FileInfo_entry:
        def __init__(self, Key):
            self.key = Key
