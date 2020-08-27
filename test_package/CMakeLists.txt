cmake_minimum_required(VERSION 3.1.0)
project(test_package)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS})

include(${CONAN_LIB_DIRS_AWS-LAMBDA-CPP}/aws-lambda-runtime/cmake/aws-lambda-runtime-config.cmake)
aws_lambda_package_target(${PROJECT_NAME})
