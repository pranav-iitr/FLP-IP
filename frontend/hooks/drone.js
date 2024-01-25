import { addQueryParams, getUrl, request } from "../utils/network";

// Mutations
export const getDrones = () => {
  const url = getUrl("/api/drone/");
  return request("GET", url, null, true);
};
export const getDrone = (id) => {
  const url = addQueryParams(getUrl(`/api/drone/`), {
    id: id,
  });
  return request("GET", url, null, true);
};
