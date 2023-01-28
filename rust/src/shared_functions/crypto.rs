use openssl::pkey::{Private, Public};
use openssl::rand::rand_bytes;
use openssl::rsa::{Padding, Rsa};
use openssl::symm::{decrypt, encrypt, Cipher};
use std::fs::File;
use std::io::{Read, Write};
use std::path::Path;

/// Openssl RSA wrapper
/// It either stores a private key (with also contains the public key), or the public key.
/// Functions that can be called depends on what key the struct has been constructed with.
pub struct Asym {
    private_key: Option<Rsa<Private>>,
    public_key: Option<Rsa<Public>>,
}

impl Asym {
    // Generate RSA public and private keys and returns an Asym struct
    pub fn new() -> Asym {
        let rsa = Rsa::generate(2048).unwrap();

        Asym {
            private_key: Some(rsa),
            public_key: None,
        }
    }

    // Load the private rsa key from a file with pem format
    pub fn load_from_priv_file(private_key_path: &str) -> Asym {
        let private_key_path = Path::new(private_key_path);

        let mut private_key_file: File = File::open(private_key_path).unwrap();
        let buffer = &mut Vec::new();
        private_key_file.read_to_end(buffer).unwrap();

        Asym::load_from_priv_pem(buffer)
    }

    // Load the private rsa key from an array of u8 with pem format
    pub fn load_from_priv_pem(private_pem: &[u8]) -> Asym {
        let private_key = Rsa::private_key_from_pem(private_pem).unwrap();

        Asym {
            private_key: Some(private_key),
            public_key: None,
        }
    }

    // Load the public rsa key from a file with pem format
    pub fn load_from_pub_file(public_key_path: &str) -> Asym {
        let public_key_path = Path::new(public_key_path);

        let mut public_key_file: File = File::open(public_key_path).unwrap();
        let buffer = &mut Vec::new();
        public_key_file.read_to_end(buffer).unwrap();

        Asym::load_from_pub_pem(buffer)
    }

    // Load the public rsa key from an array of u8 with pem format
    pub fn load_from_pub_pem(public_pem: &[u8]) -> Asym {
        let public_key = Rsa::public_key_from_pem(public_pem).unwrap();

        Asym {
            private_key: None,
            public_key: Some(public_key),
        }
    }

    // Saves the key pairs on the disk
    pub fn save_keys(&self, pub_path: &str, priv_path: &str) {
        let pub_path = Path::new(pub_path);
        let priv_path = Path::new(priv_path);

        let mut pub_file = File::create(pub_path).unwrap();
        let mut priv_file = File::create(priv_path).unwrap();

        let res = pub_file.write(
            &self
                .private_key
                .as_ref()
                .unwrap()
                .public_key_to_pem()
                .unwrap(),
        );

        let res = priv_file.write(
            &self
                .private_key
                .as_ref()
                .unwrap()
                .private_key_to_pem()
                .unwrap(),
        );
    }

    /// Encrypts data using the public rsa key, returning the encrypted text
    pub fn encrypt(&self, data: &[u8]) -> Vec<u8> {
        // Declare a buffer of the maximum size permitted by the RSA key
        let mut buf = vec![0; self.public_key.as_ref().unwrap().size() as usize];

        self.public_key
            .as_ref()
            .unwrap()
            .public_encrypt(data, &mut buf, Padding::PKCS1)
            .unwrap();

        buf
    }

    /// Decrypts data using the private rsa key, returning the decrypted text
    pub fn decrypt(&self, encrypted_text: &[u8]) -> Vec<u8> {
        // Declare a buffer of the maximum size permitted by the RSA key
        let mut decrypted_text = vec![0; self.private_key.as_ref().unwrap().size() as usize];

        let decrypted_len = self
            .private_key
            .as_ref()
            .unwrap()
            .private_decrypt(encrypted_text, &mut decrypted_text, Padding::PKCS1)
            .unwrap();

        // Trucates the additionnal bytes
        decrypted_text.truncate(decrypted_len);

        decrypted_text
    }

    // Get the public key in pem format
    pub fn get_pem_pub(&self) -> Vec<u8> {
        match self.private_key.as_ref() {
            Some(_) => {
                return self
                    .private_key
                    .as_ref()
                    .unwrap()
                    .public_key_to_pem()
                    .unwrap()
            }
            None => {
                return self
                    .public_key
                    .as_ref()
                    .unwrap()
                    .public_key_to_pem()
                    .unwrap()
            }
        }
    }

    // Get the private key in pem format
    pub fn get_pem_priv(&self) -> Vec<u8> {
        self.private_key
            .as_ref()
            .unwrap()
            .private_key_to_pem()
            .unwrap()
    }
}

/// Openssl AES wrapper
/// Stores the cipher and the symetric key
pub struct Sym {
    cipher: Cipher,
    key: Vec<u8>,
}

impl Sym {
    // Create a new symetric key
    pub fn new() -> Sym {
        let mut buf = [0; 16];
        rand_bytes(&mut buf).unwrap();

        Sym {
            cipher: Cipher::aes_128_cbc(),
            key: Vec::from(buf),
        }
    }

    // Create the struct from an existing key
    pub fn from_key(key: Vec<u8>) -> Sym {
        Sym {
            cipher: Cipher::aes_128_cbc(),
            key,
        }
    }

    // Get the key
    pub fn get_key(&self) -> &Vec<u8> {
        &self.key
    }

    // Encrypt data using the symetric key
    pub fn encrypt(&self, data: &[u8]) -> Vec<u8> {
        encrypt(self.cipher, &self.key, None, data).unwrap()
    }

    // Decrypt data using the symetric key
    pub fn decrypt(&self, data: &[u8]) -> Vec<u8> {
        decrypt(self.cipher, &self.key, None, data).unwrap()
    }
}
