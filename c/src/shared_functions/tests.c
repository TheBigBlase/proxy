//
// Created by andrewmhdb on 12/14/22.
//

#include "shared_functions.h"

int main() {
    EVP_PKEY *pkey = asymmetric_generate_keys();
    unsigned char message[] = "Salut à tous c'est Fanta\n";
    size_t message_len = strlen((const char *) &message);

    unsigned char *encrypted_message = asymmetric_encrypt(pkey, message, message_len);
    //printf("%s\n", encrypted_message);

    size_t encrypted_message_len = strlen((const char *) encrypted_message);
    unsigned char *decrypted_message = asymmetric_decrypt(pkey, encrypted_message, encrypted_message_len);
    //printf("%s\n", decrypted_message);

    FILE *private_key_file = fopen("../id_rsa", "r");
    // Seek eof
    fseek(private_key_file, 0, SEEK_END);
    long private_key_file_len = ftell(private_key_file);

    // Set cursor to the beginning of the file
    rewind(private_key_file);
    const unsigned char *private_key_buffer[private_key_file_len];
    fread(&private_key_buffer, (size_t) private_key_file_len, 1, private_key_file);

    struct evp_pkey_st *pub_key = EVP_PKEY_new();
    // Sus, bus error
    d2i_PublicKey(EVP_PKEY_RSA, &pub_key, private_key_buffer, private_key_file_len);

    BIO *bp = BIO_new_fp(stdout, BIO_NOCLOSE);
    EVP_PKEY_print_public(bp, pub_key, 0, NULL);
    BIO_free(bp);

    return 0;
}