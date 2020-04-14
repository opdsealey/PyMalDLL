# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path
from shutil import copyfile

import jinja2
import pefile

dir_path = Path(__file__).parent

# OUTPUT_FOLDER = r".\output"
TEMPLATE_FOLDER = dir_path / "templates"


class DllCreator:
    def __init__(
        self, original_dll, outfolder, template_folder=TEMPLATE_FOLDER,
    ):
        self.original_dll_name = os.path.split(original_dll)[-1]
        self.original_dll_path = original_dll
        self.outfolder = DllCreator._create_output_folder(outfolder)
        self.template_folder = Path(template_folder).absolute()
        self.templateEnv = self._create_template_env(
            template_folder=self.template_folder
        )
        self.target_dll_exported_functions = []
        self.version_info = {}
        self.parsed = {"exports": False, "version": False}
        self.internal_functions = set()

    @staticmethod
    def _create_output_folder(folder_name):
        """ Creates the folder or raises a FileExistsError
        which will buble to the cmd line """
        path = Path(folder_name).absolute()
        path.mkdir()
        return path

    @staticmethod
    def _create_template_env(template_folder):
        """
        Sets up required template renderer
        :param template_folder: (str) the path to the template folder
        :return: Template renderer for template folder
        """
        templateLoader = jinja2.FileSystemLoader(searchpath=template_folder)
        templateEnv = jinja2.Environment(loader=templateLoader)
        return templateEnv

    def render(self, function_name_stem="RedirectedFunction", unique_name=False):
        """
        Primary execution loop for rendering documents in the correct order
        """
        if not self.parsed["exports"] or not self.parsed["version"]:
            raise ValueError(
                """Exports and version info ahve not been extracted, you must call
                parse_exports and parse_version_info before rendering the output files."""
            )

        self._render_exports_def(
            function_name_stem=function_name_stem, unqiue=unique_name
        )
        self._render_dllmain()
        self._render_vcxproject()
        self._render_resource_file()

    def parse_exports(self):
        """
        Extracts the exports from the target dll
        :return: None
        """
        d = [pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_EXPORT"]]
        pe = pefile.PE(self.original_dll_path, fast_load=True)
        pe.parse_data_directories(directories=d)
        exports = [(e.ordinal, e.name) for e in pe.DIRECTORY_ENTRY_EXPORT.symbols]
        self.target_dll_exported_functions = exports
        self.parsed["exports"] = True

    def parse_version_info(self):
        """
        Extracts the dll version info
        :return:
        """
        pe = pefile.PE(self.original_dll_path)
        try:
            self.version_info["FILEFLAGSMASK"] = hex(
                pe.VS_FIXEDFILEINFO[0].FileFlagsMask
            )
            self.version_info["FILEFLAGS"] = hex(pe.VS_FIXEDFILEINFO[0].FileFlags)
            self.version_info["FILETYPE"] = "0x2L"

            self.version_info["FILEOS"] = hex(pe.VS_FIXEDFILEINFO[0].FileOS)
            for fileinfo_list in pe.FileInfo:
                for fileinfo in fileinfo_list:
                    if fileinfo.Key == b"StringFileInfo":
                        for entry in fileinfo.StringTable:
                            for k, v in entry.entries.items():
                                self.version_info[k.decode()] = v.decode()
                                if k == b"ProductVersion":
                                    self.version_info["PRODUCTVERSION"] = (
                                        v.decode().split(" ", 1)[0].replace(".", ",")
                                    )
                                elif k == b"FileVersion":
                                    self.version_info["FILEVERSION"] = (
                                        v.decode().split(" ", 1)[0].replace(".", ",")
                                    )
        except AttributeError:
            print(
                "[!] Could not pass version/file info. Info table will not be created",
                file=sys.stderr,
            )
            self.version_info = None

        self.parsed["version"] = True

    def _render_exports_def(self, function_name_stem, unqiue=False):
        """
        Creates the dll exported functions, if the unique flag is False then all
        functions will point to the same function

        :param function_name_stem: (str) the name of the function stem
        :param unqiue: (bool) create unique functions for each exported function
        :return: (None)
        """
        template = self.templateEnv.get_template("exports.def")

        exports = ""
        i = 0
        for ordinal, name in self.target_dll_exported_functions:
            if unqiue:
                func_name = "{}_{}".format(function_name_stem, i)
            else:
                func_name = function_name_stem

            self.internal_functions.add(func_name)

            if name is None:
                exports += "\t\tfunction_{}={} @ {} NONAME\n".format(
                    i, func_name, ordinal
                )

            else:
                exports += "\t\t{}={} @ {} \n".format(name.decode(), func_name, ordinal)

            i += 1

        with open(self.outfolder / "exports.def", "w") as fp:
            fp.write(template.render(exports=exports))

    def _render_resource_file(self):
        """
        Creates the resource file to include the file information in the new dll
        :return: (None)
        """
        if not self.version_info:
            # No version info in file so remove references and file
            vsxproj = self.outfolder / "MaliciousDLL.vcxproj"
            with open(vsxproj, "r") as fp:
                original = fp.readlines()

            with open(vsxproj, "w") as fp:
                for line in original:
                    if (
                        line.strip("\n").lstrip()
                        != '<ResourceCompile Include="resource.rc" />'
                    ):
                        fp.write(line)
            return

        template = self.templateEnv.get_template("resource.rc")
        with open(self.outfolder / "resource.rc", "w") as fp:
            fp.write(template.render(self.version_info))

    def _render_dllmain(self):
        """
        Creates the dll main file
        :return: (None)
        """
        exported_func_bodies = ""
        for func in self.internal_functions:
            exported_func_bodies += "VOID {}(VOID){{ return; }}\n".format(func)

        template = self.templateEnv.get_template("dllmain.c")
        with open(self.outfolder / "dllmain.c", "w") as fp:
            fp.write(template.render(exported_function_body=exported_func_bodies))

    def _render_vcxproject(self):
        """
        Updates and creates required VS project files
        :return: (None)
        """
        template = self.templateEnv.get_template("MaliciousDLL.vcxproj")
        with open(self.outfolder / "MaliciousDLL.vcxproj", "w") as fp:
            try:
                fp.write(
                    template.render(
                        TargetName=(".").join(self.original_dll_name.split(".")[:-1])
                    )
                )
            except IndexError:
                fp.write(template.render(TargetName=self.original_dll_name))

        copyfile(
            self.template_folder / "MaliciousDLL.vcxproj.user",
            self.outfolder / "MaliciousDLL.vcxproj.user",
        )

        copyfile(
            self.template_folder / "MaliciousDLL.vcxproj.filters",
            self.outfolder / "MaliciousDLL.vcxproj.filters",
        )
