use openssl::pkey::{Private, Public};
use openssl::rand::rand_bytes;
use openssl::rsa::{Padding, Rsa};
use openssl::symm::{decrypt, encrypt, Cipher};
use std::fs::File;
use std::io::{Read, Write};
use std::path::Path;

pub struct Asym {
    private_key: Option<Rsa<Private>>,
    public_key: Option<Rsa<Public>>,
}

impl Asym {
    // Generate rsa public and private keys and store them
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

        let private_key = Rsa::private_key_from_pem(buffer).unwrap();

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

        let public_key = Rsa::public_key_from_pem(buffer).unwrap();

        Asym {
            private_key: None,
            public_key: Some(public_key),
        }
    }

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

    /// Encrypts data using the public rsa key, returning the encrypted text and the number of
    /// encrypted bytes
    pub fn encrypt(&self, data: &[u8]) -> Vec<u8> {
        let mut buf = vec![0; self.public_key.as_ref().unwrap().size() as usize];
        let encrypted_len = self
            .public_key
            .as_ref()
            .unwrap()
            .public_encrypt(data, &mut buf, Padding::PKCS1)
            .unwrap();

        buf
    }

    /// Decrypts data using the private rsa key, returning the decrypted text and the number of
    /// decrypted bytes
    pub fn decrypt(&self, encrypted_text: &[u8]) -> Vec<u8> {
        let mut decrypted_text = vec![0; self.private_key.as_ref().unwrap().size() as usize];
        let decrypted_len = self
            .private_key
            .as_ref()
            .unwrap()
            .private_decrypt(encrypted_text, &mut decrypted_text, Padding::PKCS1)
            .unwrap();

        decrypted_text
    }

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

    pub fn get_pem_priv(&self) -> Vec<u8> {
        self.private_key
            .as_ref()
            .unwrap()
            .private_key_to_pem()
            .unwrap()
    }
}

pub struct Sym {
    cipher: Cipher,
    key: [u8; 16],
}

impl Sym {
    pub fn new() -> Sym {
        let mut buf = [0; 16];
        rand_bytes(&mut buf).unwrap();

        Sym {
            cipher: Cipher::aes_128_cbc(),
            key: buf,
        }
    }

    pub fn from_key(key: [u8; 16]) -> Sym {
        Sym {
            cipher: Cipher::aes_128_cbc(),
            key: key,
        }
    }

    pub fn get_key(&self) -> [u8; 16] {
        self.key
    }

    pub fn encrypt(&self, data: &[u8]) -> Vec<u8> {
        encrypt(self.cipher, &self.key, None, data).unwrap()
    }

    pub fn decrypt(&self, data: &[u8]) -> Vec<u8> {
        decrypt(self.cipher, &self.key, None, data).unwrap()
    }
}
