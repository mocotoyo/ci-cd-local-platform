from flask import Flask
import logging
from prometheus_client import Counter, generate_latest

app = Flask(__name__)

REQUESTS = Counter(
    'app_requests_total',
    'Total HTTP requests'
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

@app.route("/")
def index():
    REQUESTS.inc()
    app.logger.info("Request received")
    return "Hello CI/CD Local Platform"

@app.route("/health")
def health():
    return "OK", 200

@app.route("/metrics")
def metrics():
    return generate_latest()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

