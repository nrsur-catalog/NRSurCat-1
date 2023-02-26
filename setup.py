"""setup.py file for nrsur_catalog package."""

import os
import sys
from setuptools import find_packages, setup

NAME = "nrsur_catalog"
HERE = os.path.dirname(os.path.realpath(__file__))

# require python 3.8 or higher
if sys.version_info < (3, 8):
    raise RuntimeError("nrsur_catalog requires python 3.8 or higher")


def get_version():
    """Get the version number from the version.py file."""
    with open(f"{HERE}/src/nrsur_catalog/__init__.py") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"')


VERSION = get_version()

INSTALL_REQUIRES = [
    "matplotlib",
    "loguru",
    "bilby[gw]>=1.1.5",
]
EXTRA_REQUIRE = dict(
    dev=[
        "jupyter-book>=0.13.2",
        "zenodo_python @ git+https://github.com/avivajpeyi/zenodo-python.git@main#egg",
        "jupytext",  # for converting py-ipynb
        "ghp-import",  # for publishing to github pages
        "sphinx_inline_tabs",  # for tabs (https://sphinx-inline-tabs.readthedocs.io/en/latest/)
        "pytest",
        "GitPython"
    ]
)

setup(
    name=NAME,
    version=VERSION,
    description="NR surrogate catalog",
    author="NR Surrogate Catalog Team",
    author_email="tousif_email",
    url="nrsur_catalog_url",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={NAME: ['*/**.txt']},
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRA_REQUIRE,
    zip_safe=True,
    entry_points={
        "console_scripts": [
            f"get_nrsur_event={NAME}.api.download_event:main",
            f"build_nrsur_website={NAME}.web_builder.build_website:main",
        ]
    },
)
