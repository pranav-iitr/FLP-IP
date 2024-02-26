import { useEffect, useRef } from "react";
import io from "socket.io-client";

const VideoPlayer = (props) => {
  const videoRef = useRef();

  useEffect(() => {
    const socket = io(props?.url);
    // const room_id = room;

    socket.emit("joinRoom", props?.room);

    socket.on("stream", (data) => {
      // console.log(data)
      const img = new Image();
      img.src = `data:image/jpeg;base64,${data?.image}`;
      videoRef.className = "w-full h-[92vh]";
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
      <img className="w-full h-[90vh]" src={"/loader.gif"} ref={videoRef} />
    </div>
  );
};

export default VideoPlayer;
