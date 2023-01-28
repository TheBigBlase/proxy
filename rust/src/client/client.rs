use std::{net::TcpStream, io::Write};
use crate::shared_functions::crypto::{Asym, Sym};
use crate::shared_functions::network::read_and_parse;

// Struct storing objects to communicate with the proxy server
pub struct ProxyServer {
    stream: TcpStream,
    sym_key: Sym,
}

impl ProxyServer {
    // Connects to the proxy server and establish a secured connection
    pub fn connect(ip: &str, port: &str) -> ProxyServer {
        let mut address = String::from(ip);
        address.push(':');
        address.push_str(port);

        println!("Connecting to the proxy at: {}", address);
        let mut stream = TcpStream::connect(address).unwrap();

        // Creating new key pairs
        let asym_keys = Asym::new();

        // Saving them localy
        asym_keys.save_keys("../id_rsa.pub", "../id_rsa");

        // Sending our public key to the server
        let pub_key = asym_keys.get_pem_pub();

        println!("Sending the public key");
        stream.write(&pub_key).unwrap();

        // Getting the symetric key from the server
        let response = read_and_parse(&mut stream);

        // Decrypting the key
        let decrypted_sym_key = asym_keys.decrypt(&response);

        // Initializing Sym struct
        let sym_key = Sym::from_key(decrypted_sym_key.to_vec());

        // Sending the encrypted 'test phrase' to the server
        stream.write(&sym_key.encrypt(b"Comment est votre blanquette ?")).unwrap();

        // Getting the corresponding test phrase back
        let response = &sym_key.decrypt(&read_and_parse(&mut stream));

        // If the test phrase is not correct
        if response != b"Ma blanquette est bonne" {
            panic!("{:?}: Sym key verification did not work", stream);
        }

        ProxyServer { stream, sym_key} 
    }

    // Send a response to the server. Automatically encrypts the response.
    pub fn send_request(&mut self, request: &[u8]) {
        let message = self.sym_key.encrypt(request);
        self.stream.write(&message).unwrap();
    }

    // Waits for the server response and returns it. Automatically decrypts the response.
    pub fn wait_response(&mut self) -> Vec<u8> {
        let encrypted_response = read_and_parse(&mut self.stream);
        self.sym_key.decrypt(&encrypted_response)
    }
}
