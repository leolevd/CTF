# CTF Security Challenge

A deliberately vulnerable web application for learning and practicing security skills. This is a Capture The Flag (CTF) challenge with multiple vulnerability types to discover and exploit.

## Project Structure

```
CTF/
├── server.py                       # FastAPI server with endpoints
├── SQLManager.py                   # Database manager (vulnerable & safe functions)
├── sqlWatcher.py                   # Database viewer utility
├── randomGOODpasswordGeNeRaToR.py  # Cryptographic password generator
├── data.db                         # SQLite database
├── HTML/
│   └── docs.html                   # API Documentation
└── README.md                       # This file
```

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- SQLite3 (included with Python)

## Installation

```
bash
pip install fastapi uvicorn
```

## Running the Server

```
bash
python server.py
```

The server will start on `http://127.0.0.1:1337`

## API Documentation

Visit `http://127.0.0.1:1337/` for the API documentation.

## Intentional Vulnerabilities

This application contains **deliberate vulnerabilities** for educational purposes.

## Objective

The goal is to escalate your privileges from a regular user to `top_admin` and retrieve the secret flag from `/topadmin/secret`.


## Security Notice

**WARNING**: This application is intentionally vulnerable, but using it doesn't provide any kind of shell access or other access to your computer. Never deploy it to a public server as it is not protected from any kind of DDoS.
