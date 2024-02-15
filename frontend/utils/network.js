import axios from "axios";
import { getCookie } from "cookies-next";

export function addQueryParams(urlString, queryParams) {
  const query = Object.keys(queryParams)
    .map((k) => {
      if (Array.isArray(queryParams[k])) {
        return queryParams[k].map((val) => `${k}[]=${val}`).join("&");
      }
      return `${k}=${queryParams[k]}`;
    })
    .join("&");
  return `${urlString}?${query}`;
}

export function request(
  method,
  url,
  data,
  authorized = true,
  contentType = "application/json"
) {
  return new Promise(async (resolve, reject) => {
    let headers = { "content-type": contentType };
    const body = data;

    if (authorized) {
      const token = await getCookie("token");
      // const body = addClientIdToBody(data);
      // console.log("body =>",body);
      if (token) {
        headers.Authorization = `Bearer ${token}`;
        axios({
          method,
          url,
          body,
          headers,
          responseType: "json",
        })
          .then((res) => {
            resolve(res);
          })
          .catch((err) => {
            reject(err);
          });
      } else {
        reject("Unauthorized");
      }
    } else {
      axios({
        method,
        url,
        data,
        headers,
        responseType: "json",
      })
        .then((res) => {
          resolve(res);
        })
        .catch((err) => {
          reject(err);
        });
    }
  });
}

export const getErrorBody = (error) => {
  let response = {};
  try {
    response = error.response;
  } catch (err) {
    response = {};
  }
  response = response || {};
  const outputErrorBody = {
    ...response.data,
    status: response.status ? response.status : 408,
  };
  return outputErrorBody;
};

const get_base_api = () => {
  // let env = process.env.NODE_ENV;
  // if (env == 'production') return process.env.PRODUCTION_SERVER;
  // else if (env == 'staging')
  //   return process.env.STAGING_SERVER;

  return "http://localhost:8000";
};

export const BASE_API = get_base_api();
export const getUrl = (relUrl) => `${BASE_API}${relUrl}`;

function getBaseImgUrl() {
  let env = process.env.NODE_ENV;
  if (env === "production" || env === "staging" || env === "dev") return "";
  else {
    return "http://b.esummit.in";
  }
}

export const BASE_IMG_URL = getBaseImgUrl();
