# CTF Security Challenge

A deliberately vulnerable web application for learning and practicing security skills. This is a Capture The Flag (CTF) challenge with multiple vulnerability types to discover and exploit.

## Project Structure

• Archive_content/
-- • EasterArchive/
-- -- • dontopenmepls.zip
-- -- • easter.egg
-- -- • easteregg.txt
-- • ImportantArchive
-- -- • Greencode_greenifier_ALPHA.exe
-- -- • Greencode_greenifier.cpp
-- -- • license_transfer_agreement.md
-- -- • partnering_agreement.md
-- -- • technology_acquisition_agreement.md
• Archives/
-- • easterArchive.zip
-- • ImportantArchive.exe
• HTML/
-- • Archive_home.html
-- • docs.html
• data.db
• passwords.py
• README.md
• server.py
• SQLManager.py
• sqlWatcher.py


## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- SQLite3 (included with Python)

## Installation

```bash
pip install fastapi uvicorn
```

## Running the Server

```bash
python server.py
```

The server will start on `http://127.0.0.1:1337`

## API Documentation

Visit `http://127.0.0.1:1337/` for the API documentation.

## Intentional Vulnerabilities

This application contains **deliberate vulnerabilities** for educational purposes.

## Objective

The goal is to escalate your privileges from an outsider to `top_admin` and retrieve the secret flag from `/topadmin/secret`.
You can also consider finding the 2 easter eggs and the company's secres documents.

## Security Notice

**WARNING**: This application is intentionally vulnerable, but using it doesn't provide any kind of shell access or other access to your computer. Never deploy it to a public server as it is not protected from any kind of DDoS.
