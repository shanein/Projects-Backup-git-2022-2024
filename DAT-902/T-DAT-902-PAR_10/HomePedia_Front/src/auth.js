/*
Création de Deux Instances Axios
     Instance Authentifiée (apiAuth) : Pour les requêtes qui nécessitent un token d'authentification.
     Instance Non Authentifiée (api) : Pour les requêtes qui ne nécessitent pas d'authentification.
*/
import axios from 'axios';
// import jwt_decode from 'jwt-decode';
import store from './store';
import router from './router';
import {decodeJwt} from "@/jwtUtils";

const apiAuth = axios.create({
    baseURL: 'https://127.0.0.1:8000',
});

apiAuth.interceptors.request.use(
    async config => {
        const accessToken = store.state.accessToken;

        if (accessToken) {
            const decodedToken =  decodeJwt(accessToken);
            const currentTime = Date.now() / 1000;

            if (decodedToken.exp < currentTime) {
                try {
                    await store.dispatch('refreshToken');
                    config.headers.Authorization = `Bearer ${store.state.accessToken}`;
                } catch (err) {
                    store.dispatch('logout');
                    router.push('/account/signIn');
                }
            } else {
                config.headers.Authorization = `Bearer ${accessToken}`;
            }
        }

        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

apiAuth.interceptors.response.use(
    response => {
        return response;
    },
    async error => {
        const originalRequest = error.config;

        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                await store.dispatch('refreshToken');
                originalRequest.headers.Authorization = `Bearer ${store.state.accessToken}`;
                return apiAuth(originalRequest);
            } catch (err) {
                store.dispatch('logout');
                router.push('/account/signIn');
            }
        }

        return Promise.reject(error);
    }
);

export default apiAuth;
