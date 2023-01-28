use std::io::Read;
use std::net::TcpStream;

/// Utility function that blocks and wait for data comming from stream.
/// Reads everything and returns the buffer
pub fn read_and_parse(stream: &mut TcpStream) -> Vec<u8> {
    // Size of each buffer
    let buff_len = 2048;
    // Final buffer
    let mut buffer: Vec<u8> = Vec::new();
    let mut nb_bytes_written = buff_len;
    let mut index_end = 0;

    // Temporary buffer to read part by part
    let mut tmp_buffer = Vec::new();

    // Read bytes as long as the previous buffer was totaly full
    while nb_bytes_written == buff_len {
        // Using resize to fill the buffer with 0, as empty buffer doesn't seem to work with
        // stream.read()
        tmp_buffer.resize(buff_len, 0);

        nb_bytes_written = stream.read(&mut tmp_buffer).unwrap();
        index_end += nb_bytes_written;

        // Adding data to the final buffer
        buffer.append(&mut tmp_buffer);
    }

    // Truncate the additionnal bytes left at 0
    buffer.truncate(index_end);
    buffer
}
