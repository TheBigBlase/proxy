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

unsigned char *encrypt(EVP_PKEY *pkey, unsigned char *unencrypted_text, size_t text_len) {
    EVP_PKEY_CTX *ctx;
    ENGINE *eng = NULL;
    unsigned char *out;
    size_t outlen;

    ctx = EVP_PKEY_CTX_new(pkey, eng);

    if (!ctx)
        printf("Error, bad context");
        /* Error occurred */
    if (EVP_PKEY_encrypt_init(ctx) <= 0)
        printf("Error init");
        /* Error */
    if (EVP_PKEY_CTX_set_rsa_padding(ctx, RSA_PKCS1_OAEP_PADDING) <= 0)
        printf("Error rsa padding");
        /* Error */

    /* Determine buffer length */
    if (EVP_PKEY_encrypt(ctx, NULL, &outlen, unencrypted_text, text_len) <= 0)
        printf("Error encrypt");
        /* Error */

    out = OPENSSL_malloc(outlen);

    if (!out)
        printf("Error malloc");
        /* malloc failure */

    if (EVP_PKEY_encrypt(ctx, out, &outlen, unencrypted_text, text_len) <= 0)
        printf("Error encrypt");
        /* Error */

    /* Encrypted data is outlen bytes written to buffer out */
    return out;
}

unsigned char *decrypt(EVP_PKEY *pkey, unsigned char *encrypted_text, size_t encrypted_text_len) {
    EVP_PKEY_CTX *ctx;
    ENGINE *eng = NULL;
    unsigned char *decrypted_text;
    size_t decrypted_text_len;

    ctx = EVP_PKEY_CTX_new(pkey, eng);
    if (!ctx)
        printf("Error, bad context");
        /* Error occurred */

    if (EVP_PKEY_decrypt_init(ctx) <= 0)
        printf("Error init");
        /* Error */

    if (EVP_PKEY_CTX_set_rsa_padding(ctx, RSA_PKCS1_OAEP_PADDING) <= 0)
        printf("Error rsa padding");
        /* Error */

    /* Determine buffer length */
    if (EVP_PKEY_decrypt(ctx, NULL, &decrypted_text_len, encrypted_text, encrypted_text_len) <= 0)
        printf("Error decrypt");
        /* Error */

    decrypted_text = OPENSSL_malloc(decrypted_text_len);

    if (!decrypted_text)
        printf("Error malloc");
        /* malloc failure */

    if (EVP_PKEY_decrypt(ctx, decrypted_text, &decrypted_text_len, encrypted_text, encrypted_text_len) <= 0)
        printf("Error decrypt");
        /* Error */

    return decrypted_text;
}