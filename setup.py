from io import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

DESCRIPTION = """A tool to speed up the process of creating malicious DLLs for
side loading and search order hijacking."""
AUTHOR = "Oliver Sealey"
AUTHOR_EMAIL = "contact@carbide-security.io"
PROJECT_URLS = {
    "Documentation": "https://github.com/opdsealey/PyMalDLL/README.md",
    "Bug Tracker": "https://github.com/opdsealey/PyMalDLL/issues",
    "Source Code": "https://github.com/opdsealey/PyMalDLL",
}
INSTALL_REQUIRES = [
    "future",
    "Jinja2",
    "MarkupSafe",
    "pefile",
]
EXTRAS_REQUIRE = {"dev": ["black", "flake8", "isort", "tox", "pytest", "pre-commit"]}

setup(
    name="py-mal-dll",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    license="MIT",
    url="https://github.com/opdsealey/PyMalDLL",
    project_urls=PROJECT_URLS,
    version="0.2",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    include_package_data=True,
    # data_files=[
    #     ("license", ["LICENSE"]),
    #     (
    #         "templates",
    #         [
    #             path.join("src", "py_mal_dll", "templates", "dllmain.c"),
    #             path.join("src", "py_mal_dll", "templates", "exports.def"),
    #             path.join("src", "py_mal_dll", "templates", "resource.rc"),
    #             path.join("src", "py_mal_dll", "templates", "MaliciousDLL.vcxproj"),
    #             path.join(
    #                 "src", "py_mal_dll", "templates", "MaliciousDLL.vcxproj.filters",
    #             ),
    #             path.join(
    #                 "src", "py_mal_dll", "templates", "MaliciousDLL.vcxproj.user"
    #             ),
    #         ],
    #     ),
    # ],
)
