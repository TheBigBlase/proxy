cmake_minimum_required(VERSION 3.25)
project(proxy-c C)

set(CMAKE_C_STANDARD 99)
set(crypto
        src/shared_functions/shared_functions.c
        src/shared_functions/shared_functions.h
        )

link_libraries(-lssl -lcrypto)

add_executable(client
        src/client/main.c
        ${crypto}
        )
add_executable(server
        src/server/main.c
        ${crypto}
        )

add_executable(test_crypto
        ${crypto}
        src/shared_functions/tests.c
        )