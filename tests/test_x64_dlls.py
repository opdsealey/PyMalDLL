""" Tests for x64 Dlls """
from py_mal_dll.create_dll import DllCreator
from tests.helpers import check_output_files_exist
from tests.utils import BASE_PATH, ORIGINAL_TEMPLATE_FOLDER


# def test_no_version_info_exports(capsys, output_folder):
def test_no_version_info_exports(output_folder):
    dll_path = BASE_PATH / "resources" / "x64" / "NoVersionInfo.dll"
    creator = DllCreator(original_dll=dll_path, outfolder=output_folder)
    from os import path

    here = path.abspath(path.dirname(__file__))
    print(here)
    creator.parse_exports()
    print(ORIGINAL_TEMPLATE_FOLDER)
    print(creator.template_folder)
    # Check exports correctly recovered
    assert set(creator.target_dll_exported_functions) == set(
        [(0x60E, None), (0x60F, None), (0x610, None), (0x612, None)]
    )
    assert creator.parsed["exports"] is True
    creator.parse_version_info()
    # captured = capsys.readouterr()
    # assert (
    #     captured.err
    #     == "[!] Could not pass version/file info. Info table will not be created\n"
    # )
    assert creator.parsed["version"] is True
    assert creator.version_info is None

    creator.render()
    check_output_files_exist(output_folder=output_folder, no_resource=True)


def test_version_info_name_and_ordinal_exports(capsys, output_folder):
    dll_path = BASE_PATH / "resources" / "x64" / "NameAndOrdinal.dll"
    creator = DllCreator(
        original_dll=dll_path, outfolder=output_folder, template_folder="templates",
    )
    creator.parse_exports()
    print(creator.target_dll_exported_functions)
    assert set(creator.target_dll_exported_functions) == set(
        [
            (0x60E, None),
            (0x60F, None),
            (0x610, None),
            (0x612, None),
            (0x7B2, b"GetUnpredictedMessagePos"),
            (0x7B3, b"GetUpdateRect"),
            (0x7B4, b"GetUpdateRgn"),
            (0x7B5, b"GetUpdatedClipboardFormats"),
            (0x7B6, b"GetUserObjectInformationA"),
        ]
    )
    assert creator.parsed["exports"] is True
    creator.parse_version_info()
    captured = capsys.readouterr()
    assert captured.err == ""
    assert creator.parsed["version"] is True
    assert creator.version_info is not None

    creator.render()
    check_output_files_exist(output_folder=output_folder)
