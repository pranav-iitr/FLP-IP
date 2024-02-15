"use client";
import { useState, useEffect } from "react";
import { getCookie } from "cookies-next";
import { getDrones, getDrone } from "@/hooks/drone";
import { BASE_IMG_URL } from "@/utils/network";
import VideoPlayer from "@/components/VideoPlayer";
import { redirect } from "next/navigation";

export default function Home() {
  const [droneData, setDroneData] = useState([]);
  const [route, setRoute] = useState(0);
  const [droneUrl, setDroneUrl] = useState({});
  // const [user, setUser] = useState({});
  useEffect(() => {
    getDrones()
      .then((res) => {
        console.log(res.data);
        setDroneData(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
    const User = JSON.parse(getCookie("USER"));
    if (!User) {
      redirect("/login");
    }
    // setUser(User);
  }, []);

  return (
    <main className="flex flex-col  ">
      <div
        style={{
          boxShadow: "0px 4px 48px 0px rgba(3, 32, 32, 0.20)",
          backdropFilter: "blur(35px)",
        }}
        className=" px-12  navbar w-full h-[8vh] bg-[#1C1C1C] flex items-center justify-between "
      >
        <img className="w-9" src="/imgs/logo.png" />
        <img className="w-36" src="/imgs/white_ops.png" />
      </div>
      <div className="h-[92vh] flex justify-between">
        <div
          style={{
            boxShadow: "0px 4px 48px 0px rgba(3, 32, 32, 0.20)",
            backdropFilter: "blur(35px)",
          }}
          className="flex flex-col h-full w-[20vw] bg-[#424242] items-center "
        >
          <div
            onClick={() => {
              if (droneUrl != "") {
                setRoute(1);
              }
            }}
            style={{
              boxShadow: "0px 4px 48px 0px rgba(3, 32, 32, 0.20)",
              backdropFilter: "blur(35px)",
            }}
            className="bg-[#E4E4E4] flex items-center justify-between w-[80%] mt-8 px-4 py-1 rounded-lg cursor-pointer"
          >
            <div>Live Operations</div>{" "}
            <img className="w-12" src="/imgs/camera.png" />
          </div>
          <div
            style={{
              boxShadow: "0px 4px 48px 0px rgba(3, 32, 32, 0.20)",
              backdropFilter: "blur(35px)",
            }}
            onClick={() => {
              setRoute(0);
            }}
            className="bg-[#E4E4E4] flex items-center justify-between w-[80%] mt-4 px-4 py-1 cursor-pointer rounded-lg"
          >
            <div>Your Devices</div>{" "}
            <img className="w-12" src="/imgs/drone.png" />
          </div>
        </div>
        <div className="flex h-full w-[80vw]  ">
          {route == 0 ? (
            <>
              {droneData.length > 0 ? (
                <div>
                  {droneData.map((drone) => {
                    return (
                      <div
                        onClick={() => {
                          getDrone(drone.id)
                            .then((res) => {
                              console.log(res.data);
                              setDroneUrl(res.data);
                              console.log(droneUrl);
                              setRoute(1);
                            })
                            .catch((err) => {
                              console.log(err.message);
                            });
                        }}
                        className="flex gap-5 w-[20vw] h-[20vh] bg-[#424242] rounded-xl m-4"
                      >
                        <div className="flex gap-4 flex-col px-4 py-2">
                          <div className="text-[#fff] text-xl font-medium">
                            {drone.name}
                          </div>

                          <div>
                            <img
                              className="w-32 h-22"
                              src={`${BASE_IMG_URL}${drone.image}`}
                            />
                          </div>
                        </div>
                        <div className="flex justify-between px-4 py-2"></div>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <></>
              )}
            </>
          ) : route == 1 ? (
            <div className="m-auto ">
              <VideoPlayer room={droneUrl?.id} url={droneUrl?.url} />
            </div>
          ) : (
            <></>
          )}
        </div>
      </div>
    </main>
  );
}
