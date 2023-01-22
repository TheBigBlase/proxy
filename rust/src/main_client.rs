mod client;
mod shared_functions;
use std::io::Write;
use std::net::TcpStream;

fn main() -> std::io::Result<()> {
    let mut stream = TcpStream::connect("127.0.0.1:5303").unwrap();

    let rsa_keys = shared_functions::generate_rsa_keys("id_rsa.pub", "id_rsa").unwrap();

    let pub_key = shared_functions::load_rsa_public_key_from_file("id_rsa.pub").unwrap();

    let (message, len) = shared_functions::encrypt_rsa(pub_key, &rsa_keys.public_key_to_pem().unwrap()).unwrap();

    let res = stream.write(&message);

    Ok(())
}
