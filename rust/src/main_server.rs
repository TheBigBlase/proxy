mod server;

use std::net::TcpListener;

fn main() -> std::io::Result<()> {
    let address = String::from("127.0.0.1");
    let port = "5303";
    let address_port = address + ":" + port;
    println!("Listening on: {}", address_port);
    let listener = TcpListener::bind(address_port)?;


    // accept connections and process them serially
    for stream in listener.incoming() {
        server::handle_client(stream?);
    }

    Ok(())
}
