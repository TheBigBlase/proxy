mod shared_functions;

use shared_functions::{ Asym, Sym };
use std::path::Path;

fn main() -> std::io::Result<()> {
    let pub_path = "id_rsa.pub";
    let priv_path = "id_rsa";

    let asym = Asym::new();

    let _private_key = asym.save_keys(pub_path, priv_path);

    let asym_pub = Asym::load_from_pub_file(pub_path);
    let asym_priv = Asym::load_from_priv_file(priv_path);

    let encrypted_text = asym_pub.encrypt(b"IN RUST WE TRUST");
    println!("{:?}", String::from_utf8_lossy(&encrypted_text));

    let decrypted_text = asym_priv.decrypt(&encrypted_text);
    println!("{:?}", String::from_utf8_lossy(&decrypted_text));

    let data = b"Test symetric crypting";

    let sym = Sym::new();

    let encrypted_text_sym = sym.encrypt(data);

    println!("{:?}", String::from_utf8_lossy(&encrypted_text_sym));

    let decrypted_text_sym = sym.decrypt(encrypted_text_sym.as_slice());

    println!("{:?}", String::from_utf8_lossy(&decrypted_text_sym));

    Ok(())
}

