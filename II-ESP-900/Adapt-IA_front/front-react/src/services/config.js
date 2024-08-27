import axios from "axios";
// import { logoutUser } from "./store/authSlice";
// import { useDispatch, useSelector } from "react-redux";
import store from "./store/store";

export const apiUrl = process.env.REACT_APP_API_URL;

export const api = axios.create({
  baseURL: `${apiUrl}`,
  timeout: 5000,
});

api.interceptors.request.use(
  (config) => {
    const state = store.getState(); // Accès au store Redux
    const token = state.auth.token; // Remplacez 'auth' et 'token' par votre propre chemin dans le store

    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`; // Ajout de l'en-tête d'autorisation
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// api.interceptors.response.use(
//   (response) => response,
//   (error) => {
//     const dispatch = useDispatch();
//     if (error.response && error.response.status === 422) {
//       store.dispatch(logoutUser());
//       // localStorage.clear(); // Attention : cela nettoie tout localstorage

//       // Forcer un rafraîchissement vers /auth ?
//       // window.location.assign("/auth");
//     }
//     return Promise.reject(error);
//   }
// );
