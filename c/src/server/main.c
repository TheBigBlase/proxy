#include <stdio.h>
#include <stdbool.h>

// Global variables
int PORT = 5555;
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
                case 'p':

                default:
                    ;
            }
        }

        switch (argv[i][1]) {
            case 'p':
                ;
            case 'r':
                ;
            case 'd':
                DEBUG = true;
        }
    }
    return 0;
}
