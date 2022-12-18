//
// Created by andrewmhdb on 12/14/22.
//

#include "shared_functions.h"

int main() {
    EVP_PKEY *pkey = generate_keys();
    unsigned char message[] = "Salut à tous c'est Fanta\n";
    size_t message_len = strlen((const char *) &message);

    unsigned char *encrypted_message = encrypt(pkey, message, message_len);
    printf("%s\n", encrypted_message);

    size_t encrypted_message_len = strlen((const char *) encrypted_message);
    unsigned char *decrypted_message = decrypt(pkey, encrypted_message, encrypted_message_len);
    printf("%s\n", decrypted_message);

    return 0;
}