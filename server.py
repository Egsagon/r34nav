import time
import uuid
import scrapper
from typing import Union, Any
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
            
            ip_addr = self.client_address[0]
            print(sessions)
            # Check if there already is an instance for this session
            for sid, session in sessions.items():
                if session['ip'] == ip_addr:
                    print('Already existing session')
                    
                    # TODO choose between reseting (delete session)
                    # or handle back same uuid
                    return self.qsend(200, 'text/plain', sid.encode())
            
            sessions[new] = {
                'initialised':  time.time(),
                'ip':           self.client_address[0],
                'instance':     scrapper.Instance(new)
            }
            
            print('initialised', new)
            
            self.qsend(200, 'text/plain', new.encode())

            return
        
        else:
            session_id, args = callstring.split('/')
            type_, *args = args.split('&')
            
            args = {k: v for k, v in [el.split('=') for el in args]}
            
            # TODO
            # Remove switch case -> comprehension
            
            
            print('received request:', type_, '->', args)
            instance: scrapper.Instance = sessions[session_id]\
                ['instance']
            
            if type_ == 'query':
                # Modify the session object to be focusing on a query
                
                response = instance.do_query(args)
                
                if response is None:
                    response = 'no content found'
                
                print('got response', response)
                
                self.qsend(200, 'text/plain', response.encode())
            
            if type_ == 'next':
                # Invoke next iteration
                
                response = instance.do_next(args)
                
                print('sending', response)
                
                self.qsend(200, 'text/plain', response.encode())

            
            if type_ == 'upload':
                pass
            
            # print(session_id, '->', type_, args)
    
    def qsend(self, code: int, type_: str, text: bytes = None
                    ) -> None:
        
        self.send_response(code)
        self.send_header('content-type', type_)
        self.end_headers()
        
        if text is not None:
            self.wfile.write(text)
        
        
    
            
# List of session
sessions: dict[uuid.UUID: dict[str: Any]] = {}


if __name__ == '__main__':
    
    PORT = 8000
    server = HTTPServer(('', PORT), echoHandler)
    
    print(f'Server running on {PORT}')
    server.serve_forever()