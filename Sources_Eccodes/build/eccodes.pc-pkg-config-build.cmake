
file(READ /home/ubuntu/environment/python_grib/Sources_Eccodes/build/eccodes.pc.tmp _content)

string(REPLACE "/home/ubuntu/environment/python_grib/Sources_Eccodes/build/lib" "\${libdir}" _content "${_content}")
if(NOT "lib" STREQUAL "lib")
  string(REPLACE "/home/ubuntu/environment/python_grib/Sources_Eccodes/build/lib" "\${libdir}" _content "${_content}")
endif()
string(REPLACE "/Eccodes/lib" "\${libdir}" _content "${_content}")

file(WRITE /home/ubuntu/environment/python_grib/Sources_Eccodes/build/lib/pkgconfig/eccodes.pc "${_content}")
