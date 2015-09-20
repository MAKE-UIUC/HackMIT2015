cmake_minimum_required(VERSION 3.3)
project(3DS_VRController)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES
    src/main.c)

set(DEVKITPRO "~/devkitPro}")

set(DEVKITARM "${DEVKITPRO}/devkitARM")

set(PATH "${PATH}:${DEVKITARM}/bin:${DEVKITARM}/libexec/gcc/arm-none-eabi/4.9.2")

add_custom_target(3DS_VRController COMMAND make -C ${3DS_VRController_SOURCE_DIR}
                                            CLION_EXE_DIR=${PROJECT_BINARY_DIR})