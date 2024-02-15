"use client";
import React, { useState } from "react";
import Image from "next/image";
import toast, { Toaster } from "react-hot-toast";
import { setCookie } from "cookies-next";
import { generateOTPrequest, verifyOTPRequest } from "@/hooks/auth";
import { redirect } from 'next/navigation'

function Form() {
  const [email, setEmail] = useState("");
  const [OTP, setOTP] = useState("");
  const [otpStatus, setOtpStatus] = useState(false);
  const emailValidation = (email) => {
    const re = /\S+@\S+\.\S+/;
    return re.test(email);
  };
  const otpValidation = (otp) => {
    console.log(otp.length);
    return otp.length == 4;
  };
  return (
    <div
      style={{
        backdropFilter: "blur(35px)",
        boxShadow: "0px 4px 48px 0px rgba(3, 32, 32, 0.20)",
      }}
      className="flex w-[80vw] h-fit  "
    >
      <Toaster />
      <div>
        <Image src="/imgs/bg.png" width={600} height={160} />{" "}
      </div>
      <div className="flex  flex-col grow items-center">
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
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <div className=" w-full flex justify-end mt-4 ">
            {!otpStatus ? (
              <div
                onClick={() => {
                  if (emailValidation(email)) {
                    generateOTPrequest(email)
                      .then((res) => {
                        toast.success("OTP Sent");
                        setOtpStatus(true);
                      })
                      .catch((err) => {
                        console.log(err.message);
                        toast.error("Invalid Email");
                      });
                  } else {
                    toast.error("Invalid Email");
                  }
                }}
                className="bg-[#181818] text-[#fff] px-4 py-2 rounded-2xl cursor-pointer "
              >
                Request OTP
              </div>
            ) : (
              <></>
            )}
          </div>
          <input
            className="mt-4 w-full bg-[#FFF] backdrop-blur-lg rounded-md text-xl pl-8 py-6 rounded-m"
            placeholder="Send Otp"
            value={OTP}
            onChange={(e) => setOTP(e.target.value)}
          />
          <div
            onClick={() => {
              console.log(otpValidation(OTP), otpStatus);
              if (otpValidation(OTP) && otpStatus) {
                verifyOTPRequest({ email: email, email_otp: OTP })
                  .then((res) => {
                    toast.success("OTP Verified");
                    console.log(res);
                    setCookie("token", res.data.access_token, {
                      maxAge: 30 * 24 * 60 * 60,
                    });
                    setCookie("USER", res.data.user, {
                      maxAge: 30 * 24 * 60 * 60,
                    });
                    redirect('/')

                  })
                  .catch((err) => {
                    toast.error("Invalid OTP");
                  });
              } else {
                toast.error("Genrate OTP");
              }
            }}
            className="bg-[#181818] w-full flex mt-8 h-16 justify-center items-center text-[#fff] px-4 py-2 rounded-2xl cursor-pointer "
          >
            Submmit
          </div>
        </div>
      </div>
    </div>
  );
}

export default Form;
