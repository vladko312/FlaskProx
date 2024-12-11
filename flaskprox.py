#!/usr/bin/env python3
from flask import Flask, request
import requests
import argparse

version = "1.0.0"
options = None
app = Flask(__name__)


@app.errorhandler(404)
def proxy(_):
    global options
    if options.url:
        up = options.url
    else:
        if "host" not in request.headers and not options.upstream:
            return "No host provided", 404
        up = options.scheme if options.scheme else request.scheme
        up += "://"
        up += options.upstream if options.upstream else request.headers["host"]
        if options.upstream_port:
            up += f":{options.upstream_port}"
        up += options.path if options.path else request.path
    kwargs = {'verify': not options.insecure,
              'allow_redirects': options.redirects,
              'timeout': (options.conn_timeout, options.timeout)}
    if options.proxy:
        kwargs["proxies"] = {'http': options.proxy, 'https': options.proxy}
    response = requests.request(options.method if options.method else request.method,
                                up,
                                params=request.query_string,
                                data=request.data,
                                headers=request.headers,
                                cookies=request.cookies,
                                **kwargs)
    return response.text, response.status_code, dict(response.headers)


if __name__ == "__main__":
    print(f"""\033[94m   ______         __    \033[91m___\033[94m
  / __/ /__ ____ / /__ \033[91m/ _ \\_______ __ __\033[94m
 / _// / _ `(_-</  '_/\033[91m/ ___/ __/ _ \\\\ \\ /\033[94m
/_/ /_/\\_,_/___/_/\\_\\\033[91m/_/  /_/  \\___/_\\_\\\033[0m
                                 \033[31mv{version}\033[0m
 \033[94m*\033[0m A simple \033[91mtransparent HTTP proxy\033[0m using \033[94mFlask\033[0m
 \033[94m*\033[0m Author: \033]8;;https://github.com/vladko312\007@vladko312\033]8;;\007""")
    parser = argparse.ArgumentParser(description="FlaskProx is a transparent HTTP proxy "
                                                 "that uses Host header to determine the destination")
    parser.add_argument('-v', '--version', action='version', version=f'FlaskProx version {version}')
    server = parser.add_argument_group(title="server", description="Options for the Flask server")
    server.add_argument("-H", "--host", dest="host", default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)")
    server.add_argument("-P", "--port", dest="port", type=int, default=8080, help="Port to bind to (default: 8080)")
    server.add_argument("-D", "--debug", dest="debug", action="store_true", help="Enable Flask debug mode")
    upstream = parser.add_argument_group(title="upstream", description="Options for requests sent by proxy")
    upstream.add_argument("-p", "--proxy", dest="proxy", help="Proxy to use when connecting to upstream")
    upstream.add_argument("-i", "--insecure", dest="insecure", action="store_true",
                          help="Skip upstream SSL/TLS certificate validation")
    upstream.add_argument("-r", "--redirects", dest="redirects", action="store_true",
                          help="Follow redirects server-side, returning final result to client")
    upstream.add_argument("-t", "--timeout", dest="timeout", metavar="T", type=float, help="Upstream read timeout")
    upstream.add_argument("--ct", "--connect-timeout", metavar="T", dest="conn_timeout",
                          type=float, help="Upstream connection timeout")
    override = parser.add_argument_group(title="override", description="Override upstream request info")
    override.add_argument("--od", "--upstream-port", dest="upstream_port", metavar="PORT", type=int,
                          help="Connect to a specific upstream port")
    override.add_argument("--ou", "--url", dest="url", help="Use a specific upstream URL")
    override.add_argument("--om", "--method", dest="method", help="Force HTTP method to be used on upstream")
    override.add_argument("--os", "--scheme", dest="scheme", choices=["http", "https"],
                          help="Force HTTP or HTTPS when connecting to upstream")
    override.add_argument("--oh", "--upstream", dest="upstream", help="Use a specific upstream host")
    override.add_argument("--op", "--path", dest="path", help="Force path to be used on upstream")
    options = parser.parse_args()
    app.run(host=options.host, port=options.port, debug=options.debug)
