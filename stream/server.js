
const express = require('express');
const app = express();
const http = require('http').Server(app);
const io = require('socket.io')(http);
const port = 5000;

// Serve static files from the public directory
app.use(express.static(__dirname + '/public'));

// Route for the home page
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/public/index.html');
});

// Socket.io connection event
io.on('connection', (socket) => {
  console.log('A user connected.');

  // Join room event
  socket.on('join room', (roomId) => {
    socket.join(roomId);
    console.log('User joined room:', roomId);
  });

  // Offer event
  socket.on('offer', (offer, roomId) => {
    socket.to(roomId).emit('offer', offer);
    console.log('Sent offer to room:', roomId);
  });

  // Answer event
  socket.on('answer', (answer, roomId) => {
    socket.to(roomId).emit('answer', answer);
    console.log('Sent answer to room:', roomId);
  });

  // ICE candidate event
  socket.on('ice candidate', (candidate, roomId) => {
    socket.to(roomId).emit('ice candidate', candidate);
    console.log('Sent ICE candidate to room:', roomId);
  });

  // Disconnect event
  socket.on('disconnect', () => {
    console.log('A user disconnected.');
  });
});

// Start server
http.listen(port, () => {
  console.log(`Server running on port ${port}.`);
});