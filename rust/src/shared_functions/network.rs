use std::io::{Read, Write};
use std::net::TcpStream;

pub fn read_and_parse(stream: &mut TcpStream) -> Vec<u8> {
    let mut buffer: [u8; 2048] = [0; 2048];
    let nb_bytes_written = stream.read(&mut buffer).unwrap();
    let (res, _) = buffer.split_at(nb_bytes_written);

    res.to_vec()
}

