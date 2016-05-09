// Use SockJS
Stomp.WebSocketClass = SockJS;

// Connection parameters
var mq_username = "youweesh",
    mq_password = "upto2016",
    mq_vhost    = "/",
    mq_url      = 'http://' + window.location.hostname + ':15674/stomp',
    mq_queue = "";


// This is where we print incoming messages
var output;

var client;

function initConnection(queue, outputElement) {

    output = outputElement;
    mq_queue = queue;

    // Create a client
    client = Stomp.client(mq_url);

    // Connect to user queue
    client.connect(
        mq_username,
        mq_password,
        on_connect,
        on_connect_error,
        mq_vhost
    );

}


// This will be called upon successful connection
function on_connect() {
  output.innerHTML += 'Connected to RabbitMQ-Web-Stomp<br />';
  console.log(client);
  client.subscribe(mq_queue, on_message);
}

// This will be called upon a connection error
function on_connect_error() {
  output.innerHTML += 'Connection failed!<br />';
}

// This will be called upon arrival of a message
function on_message(m) {

    if(m.headers['type'] == "weesh")
    {
        getWeeshById(m.headers['id']);
    }
    else if(m.headers['type'] == "event")
    {
        getEventById(m.headers['id']);
    }


}


