"use client";
import { useState, useEffect } from "react";
import { getCookie, deleteCookie } from "cookies-next";
import { getDrones, getDrone } from "@/hooks/drone";
import { BASE_IMG_URL } from "@/utils/network";
import VideoPlayer from "@/components/VideoPlayer";
import { useRouter } from "next/navigation";
import Drawer from "@mui/material/Drawer";

export default function Home() {
  const [droneData, setDroneData] = useState([

  ]);
  const [route, setRoute] = useState(0);
  const [droneUrl, setDroneUrl] = useState({});
  const [open, setOpen] = useState(false);
  const router = useRouter();

  const toggleDrawer = (newState) => () => {
    console.log("toggle => ", newState);
    setOpen(newState);
  };

  useEffect(() => {
    getDrones()
      .then((res) => {
        console.log(res.data);
        setDroneData(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
    const USER = getCookie("USER");

    if (!USER) {
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
        className="px-3 mobile:px-6 tablet:px-12 navbar w-full h-[8vh] bg-[#1C1C1C] flex items-center justify-between flex-row-reverse tablet:flex-row "
      >
        <img className="w-9" src="/imgs/logo.png" />
        <img className=" w-0 tablet:w-36" src="/imgs/white_ops.png" />
        <div
          onClick={toggleDrawer(true)}
          className="flex flex-col gap-1 items-center justify-center w-12 h-12 rounded-full cursor-pointer"
        >
          <div className="bg-[#fff] h-1 w-6 rounded "></div>
          <div className="bg-[#fff] h-1 w-6 rounded "></div>
          <div className="bg-[#fff] h-1 w-6 rounded "></div>
        </div>
      </div>

      <Drawer
        sx={{
          "& .MuiPaper-root": {
            backgroundColor: "#1c1c1c",

            padding: "5px",
            boxShadow: "0px 4px 48px 0px rgba(3, 32, 32, 0.20)",
            backdropFilter: "blur(35px)",
          },
        }}
        open={open}
        onClose={toggleDrawer(false)}
      >
        <div
          style={{}}
          className="flex flex-col h-full min-w-52 w-[40vw]  items-center justify-betwen"
        >
          <div className="flex flex-col w-full items-center">
            <div
              onClick={() => {
                setOpen(false);
                if (droneUrl != "") {
                  setRoute(1);
                }
              }}
              style={{
                boxShadow: "0px 4px 48px 0px rgba(3, 32, 32, 0.20)",
                backdropFilter: "blur(35px)",
              }}
              className="bg-[#E4E4E4] flex items-center justify-between w-[90%] mt-8 px-4 py-1 rounded-lg cursor-pointer"
            >
              <div>Live Operations</div>{" "}
              <img className="w-[25%] max-w-12" src="/imgs/camera.png" />
            </div>
            <div
              style={{
                boxShadow: "0px 4px 48px 0px rgba(3, 32, 32, 0.20)",
                backdropFilter: "blur(35px)",
              }}
              onClick={() => {
                setOpen(false);
                setRoute(0);
              }}
              className="bg-[#E4E4E4] flex items-center justify-between w-[90%] mt-4 px-4 py-1 cursor-pointer rounded-lg"
            >
              <div>Your Devices</div>{" "}
              <img className="w-[25%] max-w-12" src="/imgs/Drone.png" />
            </div>
          </div>
          <div className="flex-1 flex items-end w-full justify-center">
            {" "}
            <div
              onClick={() => {
                deleteCookie("USER");
                router.push("/login");
              }}
              style={{
                boxShadow: "0px 4px 48px 0px rgba(3, 32, 32, 0.20)",
                backdropFilter: "blur(35px)",
              }}
              className="bg-[#E4E4E4] justify-center flex items-center w-[100%] mt-8 px-4 py-1  cursor-pointer"
            >
              <div>Logout</div>
            </div>{" "}
          </div>
        </div>
      </Drawer>
      <div className="h-[92vh] flex justify-between">
        <div
          style={{
            boxShadow: "0px 4px 48px 0px rgba(3, 32, 32, 0.20)",
            backdropFilter: "blur(35px)",
          }}
          className="flex flex-col h-full invisible tablet:visible w-0 tablet:w-[20vw] bg-[#424242] items-center justify-betwen"
        >
          <div className="flex flex-col w-full items-center">
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
              <img className="w-12" src="/imgs/Drone.png" />
            </div>
          </div>
          <div className="flex-1 flex items-end w-full justify-center">
            {" "}
            <div
              onClick={() => {
                deleteCookie("USER");
                router.push("/login");
              }}
              style={{
                boxShadow: "0px 4px 48px 0px rgba(3, 32, 32, 0.20)",
                backdropFilter: "blur(35px)",
              }}
              className="bg-[#E4E4E4] justify-center flex items-center w-[100%] mt-8 px-4 py-1  cursor-pointer"
            >
              <div>Logout</div>
            </div>{" "}
          </div>
        </div>
        <div className="flex h-full flex-row w-[100vw] tablet:w-[80vw]  ">
          {route == 0 ? (
            <>
              {droneData.length > 0 ? (
                <div
                  style={{
                    width: "100%",
                    display: "flex",
                    gap: "1px",
                    flexWrap: "wrap",
                    justifyContent: "space-around",
                    alignContent: "flex-start",
                    padding: "4px",
                    // background:"red",
                    height: "90vh",
                  }}
                >
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
                        className="flex gap-5 w-full max-w-52  tablet:w-[20vw] h-[20vh] bg-[#424242] rounded-xl mt-4"
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
