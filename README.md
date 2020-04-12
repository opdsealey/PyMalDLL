# Python Malicous DLL Creator (PyMalDLL)

A tool to speed up the process of creating malicous DLLs for side loading and search order hijacking. This project has been designed to run on windows systems and has not been tested on any other OS.


## Usage

```terminal
python create_dll.py --help
usage: python create_dll_cli.py --original-dll C:\Windows\System32\user32.dll --output-folder ./output

optional arguments:
  -h, --help            show this help message and exit
  --output-folder OUTPUT_FOLDER The output location
  --original-dll ORIGINAL_DLL The original dll
  --function-name FUNCTION_NAME The name given to the redirected funciton
  --unique-export-functions     If true, creates a uniquely named function for each export - WARNING: This can create VERY large .c files.

```

## Installation

1. Clone or download this repositry `git clone https://github.com/opdsealey/PyMalDLL`
2. Create a virtual envireoment, `python3 -m venv venv --prompt mal-dll` (this project currently requires python 3.8+) and activate `.\venv\Scripts\activate` 
3. Install the package `pip install .`. 

## API

### create_dll.**DllCreator**(*original_dll*,*outfolder*,*unique_exports_*=*False*,*tempate_folder*=*TEMPLATE_FOLDER*,)

Returns a `DllCreator` object after creating output folder and verifying that all required templates exist. 

*original_dll* is the path to the target dll that should be used as a base. The exports will be copied and redirected and file information will be copied into the version table resource file.

*outfolder* is the relative or absolute path to the output folder, this must not already exist and will be created upon instantiation of the class



*template_folder* the folder containing all required tempaltes, incorecctly editing files within the defualt templates folder can have breaking effects.


### DllProxyCreator.**parse_exports**(*self*)

Extracts the DLLs from the target DLL.

### DllProxyCreator.**parse_version_info**(*self*):

Extracts the dll version info


### DllProxyCreator.**render**(*self*, *function_name_stem*=*"RedirectedFunction"*, *unqiue*=*False*)

Renders the required files to create the DLL Visual Studio project. Must be called after **parse_exports** and **parse_version_info**, if they have not been called a `ValueError` is raised.

*function_name_stem* is the default name given to the function all exported functions call. If *unique* is true these will be in the form *function_name_stem_{incrementing_number}*.

*unique* if `True` each exported function will redirect to a uniquely named function, the skeleton for each function will also be created *Warning, this can make for very large and unmanagable fles.*


## Feature List

- [ ] Convert useage of `os.path` to `Pathlib`
- [ ] Allow redirected function body `.c` file to be provided.
- [ ] Functionality to create proxy DLLs
- [ ] Automatically include supplied shellcode
- [ ] Add more meaningful tests

