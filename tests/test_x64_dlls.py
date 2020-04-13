""" Tests for x64 Dlls """
from py_mal_dll.create_dll import DllCreator
from tests.utils import BASE_PATH


def test_no_version_info_exports(output_folder):
    dll_path = BASE_PATH / "resources" / "x64" / "NoVersionInfo.dll"
    creator = DllCreator(original_dll=dll_path, outfolder=output_folder)
    creator.parse_exports()

    # Check exports correctly recovered
    assert set(creator.target_dll_exported_functions) == set(
        [(0x60E, ""), (0x60F, ""), (0x610, ""), (0x612, "")]
    )
    assert creator.parsed["exports"] is True
