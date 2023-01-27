use crate::shared_functions::crypto::{Asym, Sym};
use crate::shared_functions::network::{read_and_parse};

use std::io::{Read, Write};
use std::net::TcpStream;
use std::thread;

pub fn handle_client(stream: TcpStream) {
    let handle = thread::spawn(move || {
        println!("{:?}", stream);
        let client_connection = ClientConnection::init_secure_connection(stream);


    });

    handle.join().unwrap();
}

struct ClientConnection {
    stream: TcpStream,
    sym_key: Sym,
}

impl ClientConnection {
    pub fn init_secure_connection(mut stream: TcpStream) -> ClientConnection {

        // Read the asym public key sent by the client
        let asym_pub_key = read_and_parse(&mut stream);

        // Create an asym struct 
        let asym = Asym::load_from_pub_pem(&asym_pub_key);

        // Create a sym_key
        let sym_key = Sym::new();

        // Send the sym_key encrypted with the client's public key
        stream.write(&asym.encrypt(sym_key.get_key())).unwrap();

        let response = read_and_parse(&mut stream);
        println!("{:?}", String::from_utf8_lossy(&sym_key.decrypt(&response)));

        stream.write(&sym_key.encrypt(b"Ma blanquette est bonne")).unwrap();

        ClientConnection { stream, sym_key }
    }

}

