//
// Created by andrewmhdb on 12/14/22.
//

#define OPENSSL_NO_DEPRECATED
#define OPENSSL_API_COMPAT 0x30100000L

#include "shared_functions.h"

EVP_PKEY *generate_keys() {
    /*
     * Generates public and private keys, saves them into separate files and return
     */
    EVP_PKEY *pkey = EVP_RSA_gen(1024);
    FILE *public_key_file = fopen("../id_rsa.pub", "w");
    EVP_PKEY_print_public_fp(public_key_file, pkey, 0, NULL);

    FILE *private_key_file = fopen("../id_rsa", "w");
    EVP_PKEY_print_private_fp(private_key_file, pkey, 0, NULL);
    return pkey;
}

char *encrypt(EVP_PKEY *pkey, char *message, unsigned int message_len) {
    EVP_PKEY_CTX *ctx;
    ENGINE *eng;
    unsigned char *out, *in;
    size_t outlen, inlen;

    ctx = EVP_PKEY_CTX_new(pkey, eng);

    if (!ctx)
        /* Error occurred */
    if (EVP_PKEY_encrypt_init(ctx) <= 0)
        /* Error */
    if (EVP_PKEY_CTX_set_rsa_padding(ctx, RSA_PKCS1_OAEP_PADDING) <= 0)
        /* Error */

    /* Determine buffer length */
    if (EVP_PKEY_encrypt(ctx, NULL, &outlen, in, inlen) <= 0)
        /* Error */

    out = OPENSSL_malloc(outlen);

    if (!out)
        /* malloc failure */

    if (EVP_PKEY_encrypt(ctx, out, &outlen, in, inlen) <= 0)
        /* Error */

    /* Encrypted data is outlen bytes written to buffer out */
    return NULL;
}

