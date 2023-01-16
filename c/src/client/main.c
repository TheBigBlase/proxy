#include <stdio.h>
#include <stdbool.h>
#include "../shared_functions/shared_functions.h"

// Global variables
char* IP_ADDRESS_PROXY_SERVER = {"localhost"};
bool DEBUG = false;


int main(int argc, char *argv[]) {
    // Specify that the next argument of the loop is supposed to be a value
    bool expecting_a_value = false;
    // Specify what type of value it is, e.g 'i' char would correspond to an IP address value
    char value_type = '.';

    for (int i = 0; i < argc; i++) {
        // If the previous argument is expecting a value
        if (expecting_a_value) {
            switch (value_type) {
                case 'i':
                    IP_ADDRESS_PROXY_SERVER = argv[i];
		    break;
                default:
                    break;
            }
        }

        switch (argv[i][1]) {
            case 'r':
	        break;
            case 'i':
                expecting_a_value = true;
                value_type = 'i';
		break;
            case 'd':
                DEBUG = true;
		break;
	    default:
		break;
        }
    }
    return 0;
}
