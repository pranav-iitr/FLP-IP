import { addQueryParams, getUrl, request } from "../utils/network";

// Mutations
export const generateOTPrequest = (email) => {
  const url = addQueryParams(getUrl("/api/auth/otp/"), {
    email: email,
  });

  return request("GET", url, null, false);
};
export const verifyOTPRequest = (data) => {
  console.log(data);
  const url = getUrl("/api/auth/otp/");

  return request("POST", url, data, false);
};

// export const generateOTPFunction = (successCallback, errorCallback) => {
//     return useMutation({
//         mutationFn: generateOTPrequest,
//         onSuccess: (res) => {
//             successCallback(res)
//         },
//         onError: (err) => {
//             errorCallback(err)
//         },
//     })
// }
