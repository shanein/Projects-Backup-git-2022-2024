/*
Création de Deux Instances Axios
     Instance Authentifiée (apiAuth) : Pour les requêtes qui nécessitent un token d'authentification.
     Instance Non Authentifiée (api) : Pour les requêtes qui ne nécessitent pas d'authentification.
*/

import axios from 'axios';

const api = axios.create({
    baseURL: 'https://127.0.0.1:8000',
});

export default api;
