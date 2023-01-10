/*
    app.js
*/

/*
addEventListener | `/api/next?session=${session}&page=${page}`
*/

function get(url, body = null) {
    xml = new XMLHttpRequest()
    xml.open('GET', url, false)
    xml.send(body)
    
    return xml
}

// Fetch elements
submit_query = document.querySelector('.query button')
query_field = document.querySelector('.query input')

container = document.querySelector('img')

// Initialize a new session
console.log('INITIALISING WITH API...')
UUID = get('/api/init').response
console.log('RECEIVED UUID', UUID)

// Make a query
submit_query.addEventListener('click', () => {
    raw = query_field.value

    console.log('SUBMITING QUERY', raw)
    res = get(`/api/${UUID}/query&content=${raw}`)
    console.log('RECEIVED QUERY', res.response)
})

// Fetch next url
container.addEventListener('click', () => {
    res = get(`/api/${UUID}/next`)
})

/* Handled by client:
    - download
    - previous

Handled by API:
    - init
    - querry
    - next
    - upload
*/