import os, secrets, socket, threading
from waitress import serve
import webview
os.environ.setdefault("SECRET_KEY", secrets.token_hex(32))
from app import app
with socket.socket() as s:
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
if __name__ == "__main__":
    threading.Thread(target=serve, kwargs={"app": app, "host": "127.0.0.1", "port": port}, daemon=True).start()
    webview.create_window("شركة أضواء قوة المحرك - نظام تجريبي", f"http://127.0.0.1:{port}", width=1200, height=800)
    webview.start(gui="edgechromium")
