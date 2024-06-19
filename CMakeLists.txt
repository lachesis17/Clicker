cmake_minimum_required(VERSION 3.10.0)

project(ClickerC++)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_COMPILER "C:/msys64/mingw64/bin/g++.exe")
set(CMAKE_C_COMPILER "C:/msys64/mingw64/bin/gcc.exe")
set(SOURCE_DIR "${CMAKE_SOURCE_DIR}")
#pacman -S mingw-w64-x86_64-gcc

set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_PREFIX_PATH "C:/Qt/")
include_directories("${CMAKE_PREFIX_PATH}/include")
link_directories("${CMAKE_PREFIX_PATH}/lib")

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -static-libgcc -static-libstdc++") # to bundle mingw .dll
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -static") # to bundle windows .dll

find_package(Qt5 COMPONENTS Widgets Core Gui REQUIRED)

add_executable(ClickerC++
   src/mainwindow.cpp
   src/mainwindow.h
   src/main.cpp
   src/clicker.h
   src/threadHandler.h
   assets/main_window.ui
   assets/resources.qrc
   assets/resources.rc
   ${SOURCES})

target_link_libraries(ClickerC++
   PRIVATE Qt5::Widgets
   PRIVATE Qt5::Core
   PRIVATE Qt5::Gui
)

# Post-build copy for media files
add_custom_command(TARGET ClickerC++ POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
    "${SOURCE_DIR}/assets/mouse.ico"
    $<TARGET_FILE_DIR:ClickerC++>
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
    "${SOURCE_DIR}/assets/mouse.svg"
    $<TARGET_FILE_DIR:ClickerC++>
)

if(WIN32)
    set_target_properties(ClickerC++ PROPERTIES
        WIN32_EXECUTABLE YES
    )
endif()