import { useEffect, useRef } from 'react';
import io from 'socket.io-client';

const App = () => {
  const videoRef = useRef();

  useEffect(() => {
    const socket = io('http://localhost:4000');

    socket.emit('joinRoom', "1");


    socket.on('stream', (data) => {
      console.log(data);
      const img = new Image();
      img.src = data;
      img.onload = () => {
        videoRef.current.src = img.src;
      };
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  return (
    <div>
      <h1>Camera Streaming App</h1>
      <img ref={videoRef} />
    </div>
  );
};

export default App;
