import SocketServer
import brotli
import StringIO
import gzip

class BrotliHTTPServer(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def gzipencode(self, content):
        out = StringIO.StringIO()
        f = gzip.GzipFile(fileobj=out, mode='w', compresslevel=5)
        f.write(content)
        f.close()
        return out.getvalue()

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data
        self.data = """HTTP/1.1 200 ok
                    Server: testbrotli
                    Date: Wed, 23 Sep 2015 05:52:16 GMT
                    Content-Type: text/plain
                    Connection: keep-alive
                    Content-Encoding: brotli

                    """
        self.data += brotli.compress("AAAAAAAA")
        self.request.sendall(self.data)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), BrotliHTTPServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()