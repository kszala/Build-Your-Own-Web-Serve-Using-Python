# Build Your Own Web Server Using Python

This project demonstrates how to build a web server from scratch in Python.  
It includes:  
- A **basic server** using sockets 🖧  
- A **minimal WSGI server** that can run multiple frameworks like Flask, Pyramid, and Django ⚡  

Inspired by the [Build Your Own X](https://github.com/danistefanovic/build-your-own-x) repository.

---

## 📌 1. Basic Server

The basic server shows how a server handles **HTTP requests** from a client and sends back **HTTP responses**.

- **File:** `basic_server.py`  
- **Goal:** Understand the flow of HTTP requests/responses using raw Python sockets.

### ▶️ How to Run

```bash
python basic_server.py



📌 2. WSGI Server
A minimal Python WSGI server that lets different frameworks (Flask, Pyramid, Django) run on the same server.
This demonstrates the power of WSGI.

✨ Features
WSGI server written from scratch in Python

Runs Flask, Pyramid, Django apps

Logs HTTP requests & responses

Simple, minimal, and educational

📂 Project Structure

build-your-own-wsgi/
├─ wsgi_server.py       # Custom WSGI server
├─ flask_app.py         # Flask example app
├─ pyramid_app.py       # Pyramid example app
├─ basic_server.py      # Simple socket server
├─ README.md            # Documentation
├─ .gitignore           # Ignored files

▶️ How to Run

    Clone this repo:
    git clone https://github.com/<your-username>/build-your-own-wsgi.git
    cd build-your-own-wsgi

    Run with Flask app:
    python wsgi_server.py flask_app:app

📌 Example Output

< GET /hello HTTP/1.1
< Host: localhost:8888
...
> HTTP/1.1 200 OK
> Content-Type: text/plain; charset=utf-8
> Content-Length: 28
>
> Hello world from Flask!

📖 About

This project demonstrates the WSGI standard, which makes web servers and Python frameworks work together.

By building this:

✅ You understand how Flask, Pyramid, Django work internally

✅ You can run multiple frameworks on one server

✅ You get hands-on experience with requests, responses, and headers

🔗 References

- Build Your Own X : inspiration for this project

