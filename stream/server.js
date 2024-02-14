const express = require('express');
const http = require('http');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: '*', // Replace with the origin of your React app
    methods: ["*"],
  },
});

app.use(require('cors')());

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/public/index.html');
});

io.on('connection', (socket) => {

  console.log('A user connected');

  socket.on('disconnect', () => {
    console.log('User disconnected');
  });

  socket.on('joinRoom', function (room) {
    socket.join(room);
    console.log(`User joined room: ${room}`);
  });

  socket.on('leaveRoom', function (room) {
    socket.leave(room);
    console.log(`User left room: ${room}`);
  });

  socket.on('stream', (data) => {
    // Send stream only to users in the same room
    io.to(data.room).emit('stream', data);
  });
});

server.listen(4076, () => {
  console.log('Server is running on http://localhost:4076');
});
