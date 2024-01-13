import React from "react";
import Image from "next/image";

function Form() {
  return (
    <div className="flex w-[80vw] bg-red-400 ">
      <div>
        <Image src="/imgs/bg.png" width={600} height={160} />{" "}
      </div>
      <div className="flex bg-blue-200 flex-col grow items-center">
        <div className="pt-8">
          <Image src="/imgs/Live_Ops.webp" width={240} height={60} />
        </div>
        <div
          style={{
            backdropFilter: "blur(35px)",
            boxShadow: "0px 4px 48px 0px rgba(3, 32, 32, 0.20)",
          }}
          className="w-[80%] flex items-center flex-col rounded-xl mt-8 px-16 py-5 bg-[#F0F0F0]"
        >
          <h1 className={`  font-medium text-3xl px-3 py-1 text-[#535353]`}>
            {" "}
            Log In{" "}
          </h1>
          <input
            className="mt-16 w-full bg-[#FFF] backdrop-blur-lg rounded-md text-xl pl-8 py-6 rounded-m"
            placeholder="Organization Email"
          />
          <div className=" w-full flex justify-end mt-4 ">
            {" "}
            <div className="bg-[#181818] text-[#fff] px-4 py-2 rounded-2xl cursor-pointer ">
         
              Request OTP
            </div>
          </div>
          <input
            className="mt-4 w-full bg-[#FFF] backdrop-blur-lg rounded-md text-xl pl-8 py-6 rounded-m"
            placeholder="Send Otp"
          />
          <div className="bg-[#181818] w-full flex mt-8 h-16 justify-center items-center text-[#fff] px-4 py-2 rounded-2xl cursor-pointer ">
         
         Submmit
       </div>
        </div>
      </div>
    </div>
  );
}

export default Form;
