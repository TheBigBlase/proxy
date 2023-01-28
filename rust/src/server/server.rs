use crate::shared_functions::crypto::{Asym, Sym};
use crate::shared_functions::network::read_and_parse;
use reqwest;

use std::io::Write;
use std::net::TcpStream;
use std::thread;

// Handle function called for every new connection on the server
pub fn handle_client(stream: TcpStream) {
    // Spawning a new thread and moving the TcpStream object
    let handle = thread::spawn(move || {
        println!("New connection: {:?}", stream);

        // Initialising the secure connection
        let mut client_connection = ClientConnection::init_secure_connection(stream);

        // Process each request sent by the client
        loop {
            client_connection.handle_request();
        }
    });

    handle.join().unwrap();
}

// Struct storing informations to communicate with a client
struct ClientConnection {
    stream: TcpStream,
    sym_key: Sym,
}

impl ClientConnection {
    // Process of exchanging Symetric key via the client's public key
    pub fn init_secure_connection(mut stream: TcpStream) -> ClientConnection {

        // Read the asym public key sent by the client
        let asym_pub_key = read_and_parse(&mut stream);

        // Create an asym struct from the pub key
        let asym = Asym::load_from_pub_pem(&asym_pub_key);

        // Create a sym_key
        let sym_key = Sym::new();

        // Send the sym_key encrypted with the client's public key
        stream.write(&asym.encrypt(sym_key.get_key())).unwrap();

        // Read and decrypt the 'test phrase'
        let response = &sym_key.decrypt(&read_and_parse(&mut stream));

        // If the test phrase is correct
        if response == b"Comment est votre blanquette ?" {
            // Send the corresponding response to this test phrase
            stream.write(&sym_key.encrypt(b"Ma blanquette est bonne")).unwrap();
        } else {
            panic!("{:?}: Sym key verification did not work", stream);
        }

        ClientConnection { stream, sym_key }
    }

    // Waits for a client response and returns it. Automatically decrypts the response.
    pub fn wait_response(&mut self) -> Vec<u8> {
        let response = read_and_parse(&mut self.stream);
        self.sym_key.decrypt(&response)
    }

    // Send a response to the client. Automatically encrypts the response.
    pub fn send_response(&mut self, response: &[u8]) {
        let encrypted_response = self.sym_key.encrypt(response);
        self.stream.write(&encrypted_response).unwrap();
    }

    // Waits for a client request, do the request, and send the result to the client.
    pub fn handle_request(&mut self) {
        // Wait a request
        let request = self.wait_response();
        let request_string = String::from_utf8_lossy(&request);

        let req_no_r = request_string.replace("\r", "");
        // Split lines
        let lines: Vec<&str> = req_no_r.split("\n").collect();

        let first_line = lines[0];
        let elems: Vec<&str> = first_line.split(" ").collect();
        let address = elems[1];

        println!("{:?}", first_line);

        // Do the request
        let res = reqwest::blocking::get(address).unwrap();
        
        // Send the result as bytes
        self.send_response(&res.bytes().unwrap());
    }
}

