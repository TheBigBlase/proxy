# Proxy 

This is a student assignment aiming at understanding how a proxy works, 
and how to encrypt data from the client to the proxy relatively fast.

## Phython implementation

We started by creating a maquette of the proxy using python. It helped us figuring out the right architecture of the project and also what were the main issues.

The main issues were: 
- limitations of RSA maximum length for text encryption.
- manage to support https
- usage of cryptography libraries

The python project is organized as it follows:

```
├── id_rsa                      Private key
├── id_rsa.pub                  Public key
├── main.py                     Main for server or client
├── requirements.txt            Python requirements
└── src
    ├── client
    │   └── clientMain.py       Client's code
    ├── server
    │   ├── handleClients.py    Server's client handler
    │   └── serverMain.py       Server's code
    ├── RSA.py                  RSA related code
    └── utils.py                Utility functions
```

### Running the python version 

Clone the project, go to the python folder and install the python requirements:

```bash
pip install -r requirements.txt
```
Running the proxy server:

```bash
python3 main.py --server
```

By default the server runs on the port 5555.

Running the client:

```bash
python3 main.py --client
```
Configure your browser's proxy to localhost port 1700.

## Rust implementation

After implementing the project in python, we decided to realize a version in rust. This was very ambitious from us as rust is pretty hard to get used to.

The rust project is organized as it follows:

```
├── Cargo.toml                Cargo configuration file
├── id_rsa                    Private key
├── id_rsa.pub                Public key
└── src
    ├── main_client.rs        Main file of the client
    ├── main_server.rs        Main file fo the server
    ├── test_crypto.rs        Tests for crypto functions
    ├── client
    │   └── client.rs         Client's code
    ├── server
    │   └── server.rs         Server's code
    └── shared_functions
        ├── crypto.rs         Crypto functions
        └── network.rs        Network functions
```

### Running the rust project

At first you should install rust compiler and cargo: https://www.rust-lang.org/tools/install

Rust wrapper of OpenSSL specifies that both OpenSSL libraries and headers are required to build this crate.

If not already installed: https://www.openssl.org/source/

Running the proxy server:

```bash
cargo run --bin server
```

By default the server runs on the port 28240.

Running the client:

```bash
cargo run --bin client 
```

Configure your browser's proxy to localhost port 1700.

### Encryption system

After we find out we were limited by the size of the text to be encrypted with RSA in the python version, we decided to instead
use a symmetric key for requests and response.

We implemented this process of identification:

1. The client connects to the proxy and sends his RSA public key
2. The server generates a new AES symmetric key and encrypts it with the client's public key 
3. The client decrypts the symmetric key and send a test phrase as a verification of the symmetric key
4. The server decrypts the test phrase, if it succeed, it sends back the response test phrase
5. The client decrypts the response test phrase, if it succeed, the secured authentication worked successfully

The test phrase is a simple sentence saved in plain text in the source code of both the client and the server.
The server should received "Comment est votre blanquette ?" and the client should received back "Ma blanquette est bonne", in reference to OSS 117.

### Security concerns

We are aware that our encryption process could be vulnerable to man-in-the-middle attacks. Indeed an attacker could pretend to be the proxy server, send his public key to the real proxy and then create another symmetric just for the attacked client.

Although it is very hard, as the attacker should know in advance the exact proxy software used, and the corresponding cryptography methods used.

## Improvements for the future

Rewriting this project in another language surely prevented us from implementing more features, however we were very pleased to learn Rust, and to introduce this language to our comrade.

Here is a list features that we would like to implement in the future:

- Correct support of https...
- Asynchronous version of the proxy and client using Tokio rust library
- Better command line usage experience
