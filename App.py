"""Listing Writer: a tiny local web app. Open-source AI (Gemma via Ollama) turns
a few product facts into a polished online listing. Product details and prices
never leave the seller's computer. Only the Python standard library is needed."""
import json, os, urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

MODEL = os.environ.get("MODEL", "gemma3:4b")
OLLAMA = os.environ.get("OLLAMA_URL", "http://localhost:11434")
PORT = int(os.environ.get("PORT", 8002))
HERE = os.path.dirname(os.path.abspath(__file__))

def ask_model(product, details, price, platform, tone):
    prompt = (
        "You write product listings for small online sellers.\n"
        f"Product: {product}\nDetails: {details}\nPrice: {price}\n"
        f"Where it will be posted: {platform}\nTone: {tone}\n\n"
        "Use ONLY the facts above. Never invent materials, sizes, "
        "discounts or claims that are not given.\n"
        "Reply in exactly this format:\n"
        "TITLE: (under 80 characters)\n"
        "DESCRIPTION: (80 to 120 words, short paragraphs)\n"
        "TAGS: (6 short keywords separated by commas)\n"
        "SHORT CAPTION: (one or two lines for Instagram or WhatsApp, "
        "with the price)"
    )
    body = json.dumps({"model": MODEL, "prompt": prompt, "stream": False}).encode()
    req = urllib.request.Request(f"{OLLAMA}/api/generate", body,
                                 {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)["response"]

class Handler(BaseHTTPRequestHandler):
    def _send(self, code, data, ctype="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        with open(os.path.join(HERE, "index.html"), "rb") as f:
            self._send(200, f.read(), "text/html; charset=utf-8")

    def do_POST(self):
        try:
            n = int(self.headers.get("Content-Length", 0))
            d = json.loads(self.rfile.read(n))
            text = ask_model(d["product"], d["details"], d["price"],
                             d["platform"], d["tone"])
            self._send(200, json.dumps({"listing": text}).encode())
        except Exception as e:
            msg = f"Could not reach the model. Is Ollama running? ({e})"
            self._send(500, json.dumps({"error": msg}).encode())

if __name__ == "__main__":
    print(f"Listing Writer running at http://localhost:{PORT} using {MODEL}")
    HTTPServer(("", PORT), Handler).serve_forever()