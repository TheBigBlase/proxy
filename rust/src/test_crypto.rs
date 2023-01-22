mod shared_functions;
use std::path::Path;

fn main() -> std::io::Result<()> {
    let pub_path = "id_rsa.pub";
    let priv_path = "id_rsa";

    let _private_key = shared_functions::generate_rsa_keys(pub_path, priv_path).unwrap();

    let public_key = shared_functions::load_rsa_public_key_from_file(pub_path).unwrap();
    let private_key = shared_functions::load_rsa_private_key_from_file(priv_path).unwrap();

    let (encrypted_text, len_encrypted) = shared_functions::encrypt_rsa(public_key, b"IN RUST WE TRUST").unwrap();
    println!("{:?}", String::from_utf8_lossy(&encrypted_text));

    let (decrypted_text, len_decrypted) = shared_functions::decrypt_rsa(private_key, &encrypted_text).unwrap();
    println!("{:?}", String::from_utf8_lossy(&decrypted_text));

    Ok(())
}

