#!/bin/bash


#
# (C) Copyright IBM Corp. 2021- 2023.
# https://opensource.org/licenses/BSD-3-Clause
#

# Clean up previous build artifacts
echo "Removing build & dist dirs ..."
rm -rf build dist *.egg-info

# Build package using pyproject.toml
echo "Building package ..."
python -m build
