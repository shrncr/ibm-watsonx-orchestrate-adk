#!/bin/bash


#
# (C) Copyright IBM Corp. 2021- 2023.
# https://opensource.org/licenses/BSD-3-Clause
#

echo "Removing build & dist dirs ..."
rm -r build dist ibm_watsonx_orchestrate.egg-info

echo "Building package .."

echo "include VERSION"
python setup.py sdist bdist_wheel
