from pathlib import Path

from setuptools import find_packages, setup

DESCRIPTION = """A tool to speed up the process of creating malicious DLLs for
side loading and search order hijacking."""
APP_ROOT = Path(__file__).parent
README = (APP_ROOT / "README.md").read_text()
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
    long_description=README,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    license="MIT",
    url="https://github.com/opdsealey/PyMalDLL",
    project_urls=PROJECT_URLS,
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    include_package_data=True,
    data_files=[
        ("license", ["LICENSE"]),
        (
            "templates",
            [
                "src\\py_mal_dll\\templates\\dllmain.c",
                "src\\py_mal_dll\\templates\\exports.def",
                "src\\py_mal_dll\\templates\\resource.rc",
                "src\\py_mal_dll\\templates\\MaliciousDLL.vcxproj",
                "src\\py_mal_dll\\templates\\MaliciousDLL.vcxproj.filters",
                "src\\py_mal_dll\\templates\\MaliciousDLL.vcxproj.user",
            ],
        ),
    ],
)
