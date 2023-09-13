"""Make a setup for web_builder."""

import os
from setuptools import find_packages, setup

NAME = "nrsur_catalog_webbuilder"
HERE = os.path.dirname(os.path.realpath(__file__))

INSTALL_REQUIRES = [
    "nrsur_catalog"
    "jupyter-book>=0.13.2",
    "ploomber-engine>=0.0.23",
    "tabulate",
    "jupytext",  # for converting py-ipynb
    "ghp-import",  # for publishing to github pages
    "sphinx_inline_tabs",  # for tabs (https://sphinx-inline-tabs.readthedocs.io/en/latest/)
    "pytest",
    "GitPython",
    "sphinx-inline-tabs",
    "sphinxcontrib-bibtex",
    "sphinx-argparse",
    "plotly",
    "papermill",
    "nbconvert",
    'itables',
    'pytest-mock',
]

setup(
    name=NAME,
    version="0.0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    zip_safe=True,
    entry_points={
        "console_scripts": [
            f"build_nrsur_website={NAME}.build_website:main",
            f"build_gwpage={NAME}.build_website:gwpage_main",
        ]
    },
)
