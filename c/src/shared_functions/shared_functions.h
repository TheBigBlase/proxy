//
// Created by andrewmhdb on 12/14/22.
//

#ifndef C_RSA_H
#define C_RSA_H

// Including openssl libraries
#include "openssl/ssl.h"
#include "openssl/rsa.h"
#include "openssl/evp.h"
#include "openssl/engine.h"
#include "openssl/decoder.h"

#include "string.h"

// Asymmetric functions
EVP_PKEY *asymmetric_generate_keys();
unsigned char *asymmetric_encrypt(EVP_PKEY *pkey, unsigned char *unencrypted_text, size_t text_len);
unsigned char *asymmetric_decrypt(EVP_PKEY *pkey, unsigned char *encrypted_text, size_t encrypted_text_len);

// Symmetric functions


#endif //C_RSA_H
