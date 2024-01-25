import { useEffect, useRef } from 'react';
import io from 'socket.io-client';

const VideoPlayer = () => {
  const videoRef = useRef();

  useEffect(() => {
    const socket = io('http://localhost:4000/video');

    socket.emit('joinRoom', "1");

    socket.on('video', (data) => {
      const blob = new Blob([data], { type: 'video/mp4' });
      console.log(blob)
      const videoURL = URL.createObjectURL(blob);
      videoRef.current.src = videoURL;

    });

    return () => {
      socket.disconnect();
    };
  }, []);

  return <video ref={videoRef} controls />;
};

export default VideoPlayer;
