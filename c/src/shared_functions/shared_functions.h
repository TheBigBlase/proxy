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
char *encrypt(EVP_PKEY *pkey, char *message, unsigned int message_len);

#endif //C_RSA_H
