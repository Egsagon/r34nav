/*
    app.js
*/

function get(url, body = null) {
    xml = new XMLHttpRequest()
    xml.open('GET', url, false)
    xml.send(body)
    
    return xml
}

// Fetch elements
navbar_query = document.querySelector('#query')
navbar_previous = document.querySelector('#back')
navbar_upload = document.querySelector('#upload')
//...
submit_query = document.querySelector('.query button')
query_field = document.querySelector('.query input')
query_container = document.querySelector('.query')
debug_url_field = document.querySelector('.d_url')
container = document.querySelector('img')

// Settings
received_urls = []
url_index = 0
preceding_number_of_queries = 3
max_history_lenght = 50

// Initialize a new session
console.log('INITIALISING WITH API...')
UUID = get('/api/init').response
console.log('RECEIVED UUID', UUID)

function update() {
    // Load the image from the url (index)

    // TODO Change the image too
    debug_url_field.innerHTML = received_urls[url_index] + 
    ` (${url_index})`;
    console.log(url_index, received_urls)
}

// Toggle query field
show_query = true
navbar_query.addEventListener('click', () => {
    show_query = !show_query
    query_container.style.left = show_query ? '70px' : '-100vw'

})

// Make a query
submit_query.addEventListener('click', () => {
    raw = query_field.value

    // Empty field error protection
    if (raw === '') {return null}

    res = get(`/api/${UUID}/query&content=${raw}`).response

    // Fetch the x next urls
    for (let i = 0; i < preceding_number_of_queries; i++) {
        received_urls.push(get(`/api/${UUID}/next`).response)
    }

    update()
})

// Fetch next url
container.addEventListener('click', () => {
    
    // Load the next url from ressource
    url_index ++
    update()

    // Get the last url
    res = get(`/api/${UUID}/next`).response

    // Append to the waiting list
    received_urls.push(res)

    // Remove first url if max history reached
    if (received_urls.lenght > max_history_lenght) {
        received_urls.shift()
    }
})

// Get previous url
navbar_previous.addEventListener('click', () => {

    // Error protection
    if (url_index === 0) {return alert('Reached the first image.')}
    url_index = url_index - 1
    
    update()
})

// Upload URL to the server
navbar_upload.addEventListener('click', () => {
    get(`/api/${UUID}/upload&name=auto&url=${0}`) // TODO
    // TODO
})

/* Handled by client:
    - download
    - previous  *

Handled by API:
    - init      *
    - query     *
    - next      *
    - upload
*/

