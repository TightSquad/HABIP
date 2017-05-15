#!/bin/bash

rootPythonPath="/home/pi"
tempPythonPath="${rootPythonPath}"
for dir in ${rootPythonPath}/*; do
    if [ -d $dir ]; then
        tempPythonPath="${tempPythonPath}:${dir}"
    fi
done
export PYTHONPATH="${tempPythonPath}"
