import sqlite3

conn = sqlite3.connect('./storage/base.db')
cursor = conn.cursor()

def upload(args: dict) -> None:
    '''
    Save the given url image.
    '''
    
    # id url location fetcher
    cursor.execute(
        f'''
        INSERT INTO IMAGES
        VALUES (?, ?, ?, ?)
        ''',
        (0, args['url'], args['name'], None)
    )
