from .src import app
import os

if __name__ == "__main__":
    host, port = '127.0.0.1', 9001
    if 'GMP_HOST' in os.environ:
        host = os.environ['GMP_HOST']
    if 'GMP_PORT' in os.environ:
        port = os.environ['GMP_PORT']
    from waitress import serve
    print(f"Serving at http://{host}:{port}/")
    serve(app, host=host, port=port)
