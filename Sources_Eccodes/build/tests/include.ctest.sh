set -ea
# For CMake

set -x

proj_dir=/home/ubuntu/environment/python_grib/Sources_Eccodes/eccodes-2.15.0-Source
build_dir=/home/ubuntu/environment/python_grib/Sources_Eccodes/build
data_dir=/home/ubuntu/environment/python_grib/Sources_Eccodes/build/data

# use definitions from binary dir to test if installation will be correct
def_dir="/home/ubuntu/environment/python_grib/Sources_Eccodes/build/share/eccodes/definitions"
ECCODES_DEFINITION_PATH="${def_dir}"
export ECCODES_DEFINITION_PATH

# binaries are in the TOP CMAKE_BINARY_DIR
tools_dir=/home/ubuntu/environment/python_grib/Sources_Eccodes/build/bin
tigge_dir=/home/ubuntu/environment/python_grib/Sources_Eccodes/build/bin

# If this environment variable is set, then run the
# executables with valgrind. See ECC-746
EXEC=""
if test "x$ECCODES_TEST_WITH_VALGRIND" != "x"; then
   tools_dir="valgrind --error-exitcode=1 -q /home/ubuntu/environment/python_grib/Sources_Eccodes/build/bin"
   EXEC="valgrind --error-exitcode=1 -q "
fi

# ecCodes tests are in the PROJECT_BINARY_DIR
test_dir=/home/ubuntu/environment/python_grib/Sources_Eccodes/build/tests

# use samples from binary dir to test if installation will be correct
samp_dir="/home/ubuntu/environment/python_grib/Sources_Eccodes/build/share/eccodes/samples"
ECCODES_SAMPLES_PATH=${samp_dir}
export ECCODES_SAMPLES_PATH

# Options
HAVE_JPEG=0
HAVE_LIBJASPER=0
HAVE_LIBOPENJPEG=0
HAVE_PNG=0
HAVE_AEC=0
HAVE_EXTRA_TESTS=0
HAVE_MEMFS=0

echo "Current directory: `pwd`"
