from tornado.websocket import WebSocketHandler
from tornado.web import Application, RequestHandler
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

class MainHandler(RequestHandler):
    def get(self, *args, **kwargs):
        html = '''
        <html>
            <body>
                <input type="text" id="input" />
                <button id="send">tail</button>
                <pre id="result"></pre>
            </body>
            <script>
            var result = document.getElementById('result');
            var ws = new WebSocket('ws://x.x.x.x:3000/ws')
            ws.onmessage = function(message) {
                result.innerHTML += message.data;
            }
            var input = document.getElementById("input");
            var send = document.getElementById('send');
            send.addEventListener('click', function(){
                ws.send(input.value);
            });
            </script>
        </html>
        '''
        self.write(html)

class WebTailHandler(WebSocketHandler):
    def on_message(self, message):
        print(message)
        print(print(hash(self.ws_connection)))
        for x in range(100):
            self.write_message(message)

    def on_connection_close(self):
        print(hash(self.ws_connection))

if __name__ == '__main__':
    app = Application([
        (r'/', MainHandler),
        (r'/ws', WebTailHandler)
    ])
    app.listen(3000)
    server = HTTPServer(app)
    try:
        IOLoop.current().start()
    except KeyboardInterrupt:
        IOLoop.current().stop()