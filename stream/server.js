const express = require('express');
const http = require('http');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
    cors: {
      origin: 'http://localhost:3006', // Replace with the origin of your React app
      methods: ["*"],
    },
  });
  

app.use(require('cors')())

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/public/index.html');
});

io.on('connection', (socket) => {
  console.log('A user connected');

  socket.on('disconnect', () => {
    console.log('User disconnected');
  });

  socket.on('stream', (data) => {
    io.emit('stream', data);
  });
});

// const rooms = new Map();

// io.on('connection', (socket) => {
//   console.log('A user connected');

//   socket.on('joinRoom', (videoId) => {
//     console.log("room",videoId)
//     // Get the room associated with the videoId or create a new room
//     const room = rooms.get(videoId) || videoId;

//     // Join the room
//     socket.join(room);

//     // Store room information
//     rooms.set(videoId, room);
//   });

//   socket.on('disconnect', () => {
//     console.log('User disconnected');
//   });

//   socket.on('stream', (data) => {
//     console.log(rooms)
//     // Broadcast the stream to all clients in the room
//     const [videoId, streamData] = data.split('|');
//     const room = rooms.get(videoId) || videoId;
//     io.to(room).emit('stream', streamData);
//   });
// });



server.listen(4000, () => {
  console.log('Server is running on http://localhost:4000');
});
