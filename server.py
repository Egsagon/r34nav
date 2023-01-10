import time
import uuid
import scrapper
from http.server import (
    HTTPServer,
    BaseHTTPRequestHandler
)

class echoHandler(BaseHTTPRequestHandler):
    def __init__(self, *args) -> None:
        self.last_call = time.time()
        super().__init__(*args)
    
    def do_GET(self):
        '''
        handle GET requests.
        '''
        
        print(self.path)
        
        if self.path == '/': self.path = '/index.html'
        
        if self.path.startswith('/api/'):
            if time.time() - self.last_call > 1 or 1:
                # print('api call')
            
                self.on_API_call(self.path.split('/api/')[1])
                self.last_call = time.time()
            
            return
        
        ext = self.path.split('.')[-1]
        
        exts = {
            'css': 'text/css',
            'html': 'text/html',
            'js': 'application/javascript',
            
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'json': 'application/json',
        }
        
        # Extension protection
        if ext not in exts.keys():
            msg = f'Format not supported: {ext}'
            self.send_response(400, msg)
            self.end_headers()
            self.wfile.write(msg.encode())
            return
        
        '''
        if not self.path.startswith('/client'):
            msg = f'Forbidden path: {self.path}'
            self.send_response(403, msg)
            self.end_headers()
            self.wfile.write(msg.encode())
            return
        '''
        
        self.send_response(200)
        self.send_header('content-type', exts[ext])
        self.end_headers()
    
        self.wfile.write(open(f'./client{self.path}', 'rb').read())
    
    def on_API_call(self, callstring: str) -> None:
        '''
        Handle API calls.
        
        /api/init -> return new session uuid
        
        /api/<token>/type&arg1=arg&arg2=arg -> execute <type_> for session
        '''
        
        print('cs', callstring)
        
        if callstring == 'init':
            new = str(uuid.uuid4())
            
            sessions[new] = {'initialised': time.time()}
            
            print('initialised', new)
            
            self.send_response(200)
            self.send_header('content-type', 'text/plain')
            self.end_headers()
            
            self.wfile.write(new.encode())
            
            # TODO
            # summon scrapping instance
            
            return
        
        else:
            session_id, args = callstring.split('/')
            type_, *args = args.split('&')
            
            args = {k: v for k, v in [el.split('=') for el in args]}
            
            # TODO
            # Remove switch case -> comprehension
            
            if type_ == 'query':
                # Modify the session object to be focusing on a query
                
                print('received query request:', args)
                
            if type_ == 'next':
                # Invoke next iteration
                
                print('received query request:', args)
                
                self.send_response(200)
                self.send_header('content-type', 'text/plain')
                self.end_headers()
                
                self.wfile.write('https://example.com'.encode())
            
            if type_ == 'upload':
                pass
            
            print(session_id, '->', type_, args)
            
            
# List of session
sessions: dict[uuid.UUID: dict] = {}


if __name__ == '__main__':
    
    PORT = 8000
    server = HTTPServer(('', PORT), echoHandler)
    
    print(f'Server running on {PORT}')
    server.serve_forever()