## About 
This is a chat client&server.

using `sockets` written in `python`. 

The server asks for username of client and user\chat name to connect to.

## Download
Run the following command in your terminal to save the repository in your system
> $ git clone --

## Run
### Server
> $ python main.py

### Client
> $ python  client/client.py host port

## Next features/improvements:

### Authentication
Every user is able to identify as any user.

### Scale - Threadpool
In current architecture, all threads are running in-memory of a single server instance.
In order to improve scale: support multiple instances of server-app and offload threads from running only in memory,
use a thread pool and add queues, or in more async-functions way.

### saving and loading status - DB
use external DB (or file) to save and to load chats and messages.
