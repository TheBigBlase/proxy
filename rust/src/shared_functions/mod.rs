use openssl::pkey::{Public, Private};
use openssl::error::ErrorStack;
use openssl::rsa::{Rsa, Padding};
use std::fs::File;
use std::io::{Write, Read, BufReader};
use std::path::Path;

pub fn generate_rsa_keys(pub_path: &Path, priv_path: &Path) -> Result<Rsa<Private>, ErrorStack> {
    let rsa = Rsa::generate(2048)?;
    let mut pub_file = File::create(pub_path).unwrap();
    let mut priv_file = File::create(priv_path).unwrap();

    let res = pub_file.write(&rsa.public_key_to_pem().unwrap());
    let res = priv_file.write(&rsa.private_key_to_pem().unwrap());

    Ok(rsa)
}

pub fn load_rsa_public_key(public_key_path: &Path) -> Result<Rsa<Public>, ErrorStack> {
    let mut public_key_file: File = File::open(public_key_path).unwrap();
    let buffer = &mut Vec::new();
    public_key_file.read_to_end(buffer).unwrap();

    let public_key = Rsa::public_key_from_pem(buffer)?;

    Ok(public_key)
}

/// Encrypts data using the public rsa key, returning the encrypted text and the number of
/// encrypted bytes
pub fn encrypt_rsa(key: Rsa<Public>, data: &[u8]) -> Result<(Vec<u8>, usize), ErrorStack> { 
    let mut buf = vec![0; key.size() as usize];
    let encrypted_len = key.public_encrypt(data, &mut buf, Padding::PKCS1)?;

    Ok((buf, encrypted_len))
}

/// Decrypts data using the private rsa key, returning the decrypted text and the number of
/// decrypted bytes
pub fn decrypt_rsa(key: Rsa<Private>, encrypted_text: &[u8]) -> Result<(Vec<u8>, usize), ErrorStack> { 
    
    let mut decrypted_text = vec![0; key.size() as usize];
    let decrypted_len = key.private_decrypt(encrypted_text, &mut decrypted_text, Padding::PKCS1)?;

    Ok((decrypted_text, decrypted_len))
}
