FlaskProx
=========
[![Version 1.0](https://img.shields.io/badge/version-1.0-green.svg?logo=github)](https://github.com/vladko312/flaskprox)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg?logo=python)](https://www.python.org/downloads/release/python-3130/)
[![Python 3.6](https://img.shields.io/badge/python-3.6+-yellow.svg?logo=python)](https://www.python.org/downloads/release/python-360/)
[![GitHub](https://img.shields.io/github/license/vladko312/flaskprox?color=green&logo=gnu)](https://www.gnu.org/licenses/gpl-3.0.txt)
[![GitHub last commit](https://img.shields.io/github/last-commit/vladko312/flaskprox?color=green&logo=github)](https://github.com/vladko312/flaskprox/commits/)
[![Maintenance](https://img.shields.io/maintenance/yes/2025?logo=github)](https://github.com/vladko312/flaskprox)

**_FlaskProx_** is a simple transparent HTTP proxy, which uses `Host` HTTP header to determine the upstream server. This proxy is using **Flask** WSGI server, which simplifies deployment.

This tool was created mainly for information security research, but it could be used as a regular transparent proxy for many other tasks.

Features
--------
- `Host` header upstream detection
- Easy deployment using Flask
- Configuration through CLI options
- Upstream HTTP proxy support
- Server-side redirect processing
- Overriding upstream parameters
- Connection and reading timeouts
- SSL/TLS certificate validation
- Easy to modify code

Usage
-----
Read help message with all CLI options:
```shell
python3 flaskprox.py -h
```
Run the FlaskProx server on port 1337:
```shell
python3 flaskprox.py -P 1337
```