cmake_minimum_required(VERSION 3.20)
project(pbr_raytracer CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_executable(raytracer
    src/main.cpp
    src/vec3.h
    src/ray.h
    src/interval.h
    src/color.h
    src/rtweekend.h
    src/hittable.h
    src/hittable_list.h
    src/sphere.h
    src/camera.h
    src/material.h
)

target_compile_options(raytracer PRIVATE /utf-8)

# 출력 폴더 경로를 컴파일 타임에 박아넣어 IDE 별 CWD 차이를 무력화한다
target_compile_definitions(raytracer PRIVATE
    PROJECT_SOURCE_DIR="${CMAKE_SOURCE_DIR}"
)

add_custom_command(TARGET raytracer POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E make_directory
    ${CMAKE_SOURCE_DIR}/output
)
