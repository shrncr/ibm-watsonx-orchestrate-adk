#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from setuptools import setup, find_packages
import os

with open("VERSION", "r") as f_ver:
    VERSION = f_ver.read()

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="ibm_watsonx_orchestrate",
    version=VERSION,
    python_requires=">=3.10",
    author="IBM",
    author_email="abc@ibm.com",
    description="IBM watsonx.orchestrate SDK",
    long_description=long_description,
    # long_description_content_type="text/markdown",
    license="BSD-3-Clause",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: English",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Internet",
    ],
    keywords=[
        "watsonx.orchestrate",
        "AI Agents",
        "IBM",
        "Generative AI",
        "client",
        "API",
    ],
    url="https://ibm.github.io/watsonx-orchestrate-python-sdk",
    packages=find_packages(exclude=["tests.*", "tests"]),
    # package_data={
    #     "": ["messages/messages_en.json"],
    #     "api_version_param": ["utils/API_VERSION_PARAM"],
    # },
    install_requires=[
        "requests",
        "urllib3",
        "certifi",
        "pandas",
        "tabulate",
        "packaging",
        "importlib-metadata",
    ],
    include_package_data=True,
)
