mod client { pub mod client; }
mod shared_functions { pub mod crypto; pub mod network; }

use std::io::{ Write, Read };
use std::net::{ TcpStream, TcpListener };
use client::client::ProxyConnection;

fn main() -> std::io::Result<()> {
        
    let proxy_connection = ProxyConnection::connect("127.0.0.1", "28240");

    let address_browser = "localhost:1700";
    println!("Listening browser on: {}", address_browser);
    let browser_listener = TcpListener::bind(address_browser)?;

    loop {
        let (mut file_descriptor, _) = browser_listener.accept().unwrap();

        let mut buf: [u8; 4096] = [0; 4096];
        let nb_bytes_written = file_descriptor.read(&mut buf).unwrap();

        println!("{:?}", String::from_utf8_lossy(&buf));
    }
}
