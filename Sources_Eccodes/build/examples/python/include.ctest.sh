# examples/python include file for CMake

set -eax

data_dir=/home/ubuntu/environment/python_grib/Sources_Eccodes/build/data

# use definitions from binary dir to test if installation will be correct
def_dir="/home/ubuntu/environment/python_grib/Sources_Eccodes/build/share/eccodes/definitions"
ECCODES_DEFINITION_PATH="${def_dir}"
export ECCODES_DEFINITION_PATH

tools_dir=/home/ubuntu/environment/python_grib/Sources_Eccodes/build/bin
examples_dir=/home/ubuntu/environment/python_grib/Sources_Eccodes/build/examples/python
examples_src=/home/ubuntu/environment/python_grib/Sources_Eccodes/eccodes-2.15.0-Source/examples/python

# use samples from binary dir to test if installation will be correct
samp_dir="/home/ubuntu/environment/python_grib/Sources_Eccodes/build/share/eccodes/samples"
ECCODES_SAMPLES_PATH=${samp_dir}
export ECCODES_SAMPLES_PATH

PYTHONPATH=/home/ubuntu/environment/python_grib/Sources_Eccodes/build/python3:$PYTHONPATH
export PYTHONPATH

echo "Current directory: `pwd`"
