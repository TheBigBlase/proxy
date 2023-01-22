use std::io::Read;
use std::net::TcpStream;
use std::thread;

pub fn handle_client(stream: TcpStream) {
    let handle = thread::spawn(move || {
        println!("{:?}", stream);

        let buf: &mut [u8];

        stream.read(buf);

    });

    handle.join().unwrap();
}

