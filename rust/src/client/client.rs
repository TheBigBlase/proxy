use std::{net::{TcpListener, TcpStream}, io::{Write, Read, BufRead}};
use std::convert::TryInto;

use crate::shared_functions::crypto::{Asym, Sym};
use crate::shared_functions::network::{read_and_parse};


pub struct ProxyConnection {
    stream: TcpStream,
    asym_keys: Asym,
    sym_key: Sym,
}

impl ProxyConnection {
    // Connects to the proxy server
    pub fn connect(ip: &str, port: &str) -> ProxyConnection {
        let mut address = String::from(ip);
        address.push(':');
        address.push_str(port);

        println!("Connecting to the proxy at {}", address);
        let mut stream = TcpStream::connect(address).unwrap();

        // Creating new key pairs
        let asym_keys = Asym::new();

        // Saving them localy
        asym_keys.save_keys("../id_rsa.pub", "../id_rsa");

        // Sending our public key to the server
        let pub_key = asym_keys.get_pem_pub();

        println!("Sending the public key");

        stream.write(&pub_key).unwrap();

        // Getting the symetric key
        let response = read_and_parse(&mut stream);

        // Decrypting the key
        let decrypted_sym_key = asym_keys.decrypt(&response);

        let sym_key = Sym::from_key(decrypted_sym_key.to_vec());

        // Sending the encrypted 'test phrase' of the symetric key
        stream.write(&sym_key.encrypt(b"Comment est votre blanquette ?")).unwrap();

        let response = read_and_parse(&mut stream);

        println!("{:?}", String::from_utf8_lossy(&sym_key.decrypt(&response)));

        ProxyConnection { stream, asym_keys, sym_key} 
    }
}
