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

#include "string.h"


EVP_PKEY *generate_keys();
unsigned char *encrypt(EVP_PKEY *pkey, unsigned char *unencrypted_text, size_t text_len);
unsigned char *decrypt(EVP_PKEY *pkey, unsigned char *encrypted_text, size_t encrypted_text_len);

#endif //C_RSA_H
