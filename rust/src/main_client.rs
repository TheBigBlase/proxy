mod client {
    pub mod client;
}
mod shared_functions {
    pub mod crypto;
    pub mod network;
}

use client::client::ProxyServer;
use std::io::{Read, Write};
use std::net::TcpListener;

fn main() -> std::io::Result<()> {
    // Connecting to the proxy server
    let mut proxy_server = ProxyServer::connect("127.0.0.1", "28240");

    let address_browser = "localhost:1700";

    // Connecting to the browser
    let browser_listener = TcpListener::bind(address_browser)?;
    println!("Listening browser on: {}", address_browser);

    loop {
        // Accept a request from the browser
        let (mut file_descriptor, _) = browser_listener.accept().unwrap();

        let mut buf: [u8; 4096] = [0; 4096];

        // Read the request
        let nb_bytes_written = file_descriptor.read(&mut buf).unwrap();
        let (request, _) = buf.split_at(nb_bytes_written);

        println!("Request: {:?}", String::from_utf8_lossy(&request));

        // Sends the request to the proxy
        proxy_server.send_request(&request);

        // Gets the result
        let response = proxy_server.wait_response();

        // Sends the result to the browser
        file_descriptor.write(&response).unwrap();
    }
}
