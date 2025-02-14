// api/user.js
import axios from "axios";

export const updateProfile = async (data) => {
  return axios.put("/api/profile/update", data, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("access_token")}`, // Używamy tokena do autoryzacji
    },
  });
};
