#HTTP Cache Poisoning Tester

A Python-based security testing tool designed to probe web servers by inserting the X-Forwarded-Proto header to test for cache poisoning attacks

#📋 Overview

This tool sends specially crafted HTTP requests to test how web servers handle cache-busting parameters and HTTP/HTTPS protocol transitions. It's particularly useful for:

Testing CDN and reverse proxy configurations
Identifying cache poisoning vulnerabilities
Detecting HTTP protocol downgrade issues
Security research and penetration testing

🔧 Features

Dual Request Types: Tests both baseline requests and modified requests with X-Forwarded-Proto header
Cache Busting: Automatically generates random cache-busting parameters
Concurrent Testing: Multi-threaded execution with configurable worker pool (default: 200 threads)
Proxy Support: Built-in HTTP proxy integration for traffic inspection
Raw HTTP Requests: Uses low-level raw HTTP request construction for precise control

📦 Requirements

Dependencies

pip install requests
pip install requests-raw
pip install urllib3

Python Version

Python 3.6+
🚀 Installation

Clone or download the script
Install dependencies:
pip install -r requirements.txt

Create an input file with target hosts
💻 Usage

Basic Command

python script.py -i input.txt -o results.txt

Command-Line Arguments

Argument	Short	Required	Default	Description
--input	-i	Yes	-	Input file containing target hosts (one per line)
--output	-o	No	output	Output file for results
Input File Format

Create a text file with one hostname per line:

example.com
test.example.org
app.company.com

🔍 How It Works

Request Types

Base Request (testcheck)

Tests with standard HTTPS request
Path: /testcheck.js?cache_buster=testcheck
No protocol modification headers
Modified Request (random cache buster)

Includes X-Forwarded-Proto: http header
Tests for HTTP protocol downgrade handling
Path: /{random}.js?cache_buster={random}
Request Flow

For each host:
  1. Send base request with fixed cache buster
  2. Generate random 5-character cache buster
  3. Send modified request with X-Forwarded-Proto header
  4. Log status codes and responses

⚙️ Configuration

Proxy Settings

The tool includes proxy configuration for traffic inspection (e.g., Burp Suite):

HTTP_PROXY = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

To disable proxy:

Comment out the proxy parameter in requests_raw.raw() calls
Change proxies=HTTP_PROXY to proxies=None
Thread Pool Size

Adjust concurrent requests by modifying:

MAX_THREADS = 200  # Reduce for slower networks or to avoid rate limiting

📊 Output

The tool outputs real-time results to console:

example.com/testcheck.js?cache_buster=testcheck 200
example.com/a3b9f.js?cache_buster=a3b9f 302
test.example.org/testcheck.js?cache_buster=testcheck 404

Format: {host}/{path} {status_code}

🛡️ Security Considerations

What This Tests

Cache Poisoning: Can attackers inject cached responses?
Protocol Downgrade: Does the server respect X-Forwarded-Proto?
CDN Misconfiguration: Are there bypasses through cache variations?
HTTPS Enforcement: Can HTTPS be downgraded to HTTP?
Common Vulnerabilities Detected

Cache poisoning via unkeyed headers
HTTP/HTTPS mismatch handling
Inconsistent redirect behavior
Missing security headers on cached content
🐛 Troubleshooting

Connection Timeouts

If you experience timeouts:

Reduce MAX_THREADS to lower concurrency
Increase timeout value (currently 5 seconds)
Check network connectivity and firewall rules
Request Failures

Common causes:

Invalid hostnames in input file
Network connectivity issues
Rate limiting by target servers
Proxy configuration errors
📝 Example Session

$ python cache_buster.py -i targets.txt -o results.txt
example.com/testcheck.js?cache_buster=testcheck 200
example.com/k7m2p.js?cache_buster=k7m2p 200
api.example.com/testcheck.js?cache_buster=testcheck 404
api.example.com/x9q4n.js?cache_buster=x9q4n 404
Execution time: 3.45 seconds
