# CMake generated Testfile for 
# Source directory: /home/ubuntu/environment/python_grib/Sources_Eccodes/eccodes-2.15.0-Source/examples/F90
# Build directory: /home/ubuntu/environment/python_grib/Sources_Eccodes/build/examples/F90
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(eccodes_f_grib_set_pv "/home/ubuntu/environment/python_grib/Sources_Eccodes/eccodes-2.15.0-Source/examples/F90/grib_set_pv.sh")
set_tests_properties(eccodes_f_grib_set_pv PROPERTIES  ENVIRONMENT "OMP_NUM_THREADS=1" LABELS "eccodes;script")
add_test(eccodes_f_grib_set_data "/home/ubuntu/environment/python_grib/Sources_Eccodes/eccodes-2.15.0-Source/examples/F90/grib_set_data.sh")
set_tests_properties(eccodes_f_grib_set_data PROPERTIES  ENVIRONMENT "OMP_NUM_THREADS=1" LABELS "eccodes;script")
add_test(eccodes_f_grib_ecc-671 "/home/ubuntu/environment/python_grib/Sources_Eccodes/eccodes-2.15.0-Source/examples/F90/grib_ecc-671.sh")
set_tests_properties(eccodes_f_grib_ecc-671 PROPERTIES  ENVIRONMENT "OMP_NUM_THREADS=1" LABELS "eccodes;script")
