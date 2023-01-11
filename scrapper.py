import json
import requests
import base_handler as dbase
from bs4 import BeautifulSoup as bs

vault = json.load(open('vault.json'))

def query(text: str, page: int = 0) -> list[str]:
    '''
    '''
    
    text = '+'.join(text.split())
    
    # 42 = number of images per page
    page = f'&pid={page * 42}' if page else ''
    
    url = vault['url'] + f'index.php?page=post&s=list&tags={text}{page}'
    
    # Fetch page
    res = requests.get(url)
    if res.status_code != 200: raise Exception('Failed to access website.')
    
    soup = bs(res.content, 'html.parser');
    
    for image in soup.find_all('span', {'class': 'thumb'}):

        # Get image id
        id_ = image.get('id')[1:]

        # Fetch target image html page
        ires = requests.get(vault['img'] + id_)
        if res.status_code != 200: raise Exception('Failed to access website.')

        # Fetch target url
        
        isoup = bs(ires.content, 'html.parser')
        
        iurl = None
        img = isoup.find('img', attrs = {'id': 'image'})
        
        if img is None: iurl = isoup.find('video').get('src')
        
        else: iurl = img.get('src')
        
        yield iurl

def fetch(url: str, path: str) -> bytes:
    '''
    '''
    
    ext = url.split('.')[-1].split('?')[0]
    
    # Fetch bytes
    file = requests.get(url)
    if file.status_code != 200: raise Exception('Cannot access url.')
    
    # Write to file
    # with open(f'{path}.{ext}', 'wb') as f: f.write(file.content)
    
    # return bytes
    return file.content



class Instance:
    def __init__(self, uuid: str) -> None:
        '''
        Represent an instance of the scrapper assigned to
        a client instance.
        '''
        
        self.uuid = uuid
        self.current_query = None # type generator
        self.raw_query: str = None
        self.page = 0
        
        self.url_list: list[str] = []
        
    def do_query(self, args: dict = {}) -> str:
        '''
        Create a new query to the target and return the
        first url.
        '''
        
        self.raw_query = args.get('content', self.raw_query)
        self.page = args.get('page', self.page)
        
        if self.raw_query is None: raise Exception('Emtpy query')
        
        self.current_query = query(self.raw_query, self.page)
        
        return self.do_next()
    
    def do_next(self, args: dict = {}) -> str:
        '''
        Returns the next url to watch.
        '''
        
        try:
            url = next(self.current_query)
            self.url_list += [url]
            return url

        except StopIteration:
            # Reached the end of query, create a
            # new one on next page
            
            self.page += 1
            return self.do_query()
    
    def do_upload(self, args: dict = {}) -> bool:
        '''
        Save and upload the given image url and update the database.
        
        Format:
            /api/upload&name=1&url=https://example.com
        '''
        
        path = './storage/' + args['name'].replace('/', '')
        with open(path, 'wb') as f: f.write(requests.get(args['url']))
        
        args['name'] = path
        dbase.upload(args)
        
        
        
        
    
    # HANDLED BY CLIENT (with ~50 history list)
    # def do_prev(self) -> str: pass
    