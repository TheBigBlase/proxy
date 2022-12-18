#include <stdio.h>
#include <stdbool.h>
#include "../crypto/crypto_funcs.h"

// Global variables
char* IP_ADDRESS_PROXY_SERVER = {"localhost"};
bool DEBUG = false;


int main(int argc, char *argv[]) {
    // Specify that the next argument of the loop is supposed to be a value
    bool expecting_a_value = false;
    // Specify what type of value it is, e.g 'i' char would correspond to an IP address value
    char value_type = '.';

    for (int i; i < argc; i++) {
        // If the previous argument is expecting a value
        if (expecting_a_value) {
            switch (value_type) {
                case 'i':
                    IP_ADDRESS_PROXY_SERVER = argv[i];
                default:
                    ;
            }
        }

        switch (argv[i][1]) {
            case 'r':

            case 'i':
                expecting_a_value = true;
                value_type = 'i';
            case 'd':
                DEBUG = true;
        }
    }
    return 0;
}
