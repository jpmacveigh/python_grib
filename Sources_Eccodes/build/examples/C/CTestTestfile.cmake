# CMake generated Testfile for 
# Source directory: /home/ubuntu/environment/python_grib/Sources_Eccodes/eccodes-2.15.0-Source/examples/C
# Build directory: /home/ubuntu/environment/python_grib/Sources_Eccodes/build/examples/C
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(eccodes_c_grib_multi "/home/ubuntu/environment/python_grib/Sources_Eccodes/eccodes-2.15.0-Source/examples/C/grib_multi.sh")
set_tests_properties(eccodes_c_grib_multi PROPERTIES  ENVIRONMENT "OMP_NUM_THREADS=1" LABELS "eccodes;script")
add_test(eccodes_c_grib_set_data "/home/ubuntu/environment/python_grib/Sources_Eccodes/eccodes-2.15.0-Source/examples/C/grib_set_data.sh")
set_tests_properties(eccodes_c_grib_set_data PROPERTIES  ENVIRONMENT "OMP_NUM_THREADS=1" LABELS "eccodes;script")
add_test(eccodes_c_large_grib1 "/home/ubuntu/environment/python_grib/Sources_Eccodes/eccodes-2.15.0-Source/examples/C/large_grib1.sh")
set_tests_properties(eccodes_c_large_grib1 PROPERTIES  ENVIRONMENT "OMP_NUM_THREADS=1" LABELS "eccodes;script")
add_test(eccodes_c_grib_sections_copy "/home/ubuntu/environment/python_grib/Sources_Eccodes/eccodes-2.15.0-Source/examples/C/grib_sections_copy.sh")
set_tests_properties(eccodes_c_grib_sections_copy PROPERTIES  ENVIRONMENT "OMP_NUM_THREADS=1" LABELS "eccodes;script")
add_test(eccodes_c_get_product_kind_samples "/home/ubuntu/environment/python_grib/Sources_Eccodes/eccodes-2.15.0-Source/examples/C/get_product_kind_samples.sh")
set_tests_properties(eccodes_c_get_product_kind_samples PROPERTIES  ENVIRONMENT "OMP_NUM_THREADS=1" LABELS "eccodes;script")
add_test(eccodes_c_new_sample "/home/ubuntu/environment/python_grib/Sources_Eccodes/build/examples/C/eccodes_c_new_sample" "out.grib")
set_tests_properties(eccodes_c_new_sample PROPERTIES  ENVIRONMENT "ECCODES_SAMPLES_PATH=/home/ubuntu/environment/python_grib/Sources_Eccodes/eccodes-2.15.0-Source/samples;ECCODES_DEFINITION_PATH=/home/ubuntu/environment/python_grib/Sources_Eccodes/eccodes-2.15.0-Source/definitions;OMP_NUM_THREADS=1" LABELS "eccodes;executable")
