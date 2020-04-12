# -*- coding: utf-8 -*-
from py_mal_dll.create_dll import DllCreator
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create Side-loading dll for use with implants"
    )
    parser = argparse.ArgumentParser(
        usage=r"python create_dll_cli.py --original-dll C:\Windows\System32\user32.dll --output-folder ./output"
    )
    parser.add_argument(
        "--output-folder",
        dest="output_folder",
        action="store",
        help="The output location",
        required=True,
    )
    parser.add_argument(
        "--original-dll",
        dest="original_dll",
        action="store",
        help="The original dll",
        required=True,
    )
    parser.add_argument(
        "--function-name",
        dest="function_name",
        default="RedirectedExecution",
        action="store",
        help="The name given to the redirected funciton",
        required=False,
    )
    parser.add_argument(
        "--unique-export-functions",
        dest="unique_export_functions",
        action="store_true",
        help="If true, creates a uniquely named function for each export - WARNING: This can create VERY large .c files.",
    )

    args = parser.parse_args()

    creator = DllCreator(original_dll=args.original_dll, outfolder=args.output_folder,)

    creator.parse_exports()
    creator.parse_version_info()
    creator.render(
        function_name_stem=args.function_name, unique_name=args.unique_export_functions
    )
