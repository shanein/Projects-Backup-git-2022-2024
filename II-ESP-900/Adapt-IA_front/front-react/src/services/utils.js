// import { logoutUser } from "./store/authSlice";

export const sanitizeInput = (input) => {
  return input
    .replace(/\\/g, "\\\\")
    .replace(/\$/g, "\\$")
    .replace(/'/g, "\\'")
    .replace(/"/g, '\\"');
};

export const convertDateTimeToDate = (dateTime) => {
  const date = new Date(dateTime);
  const dateString = date.toISOString().split("T")[0]; // Cela donnera "2023-11-18" pour votre exemple
  return dateString;
};

// Fonction pour générer une clé de cryptage
// export async function generateKey() {
//   const key = await window.crypto.subtle.generateKey(
//     {
//       name: "AES-GCM",
//       length: 256,
//     },
//     true,
//     ["encrypt", "decrypt"]
//   );
//   return key;
// }

// Fonction pour crypter les données
// export async function encryptData(secretData, key) {
//   const encodedData = new TextEncoder().encode(secretData);
//   const encryptedData = await window.crypto.subtle.encrypt(
//     {
//       name: "AES-GCM",
//       iv: window.crypto.getRandomValues(new Uint8Array(12)),
//     },
//     key,
//     encodedData
//   );
//   return encryptedData;
// }

// Fonction pour décrypter les données
// export async function decryptData(encryptedData, key) {
//   const decryptedData = await window.crypto.subtle.decrypt(
//     {
//       name: "AES-GCM",
//       iv: window.crypto.getRandomValues(new Uint8Array(12)),
//     },
//     key,
//     encryptedData
//   );
//   const decodedData = new TextDecoder().decode(decryptedData);
//   return decodedData;
// }

export const dayNames = [
  "lundi",
  "mardi",
  "mercredi",
  "jeudi",
  "vendredi",
  "samedi",
  "dimanche",
];

export const dayNamesShort = ["lun", "mar", "mer", "jeu", "ven", "sam", "dim"];

export const dayNamesMin = ["L", "M", "M", "J", "V", "S", "D"];

export const monthNames = [
  "janvier",
  "février",
  "mars",
  "avril",
  "mai",
  "juin",
  "juillet",
  "août",
  "septembre",
  "octobre",
  "novembre",
  "décembre",
];

export const monthNamesShort = [
  "janv",
  "fev",
  "mars",
  "avr",
  "mai",
  "juin",
  "juil",
  "aout",
  "sept",
  "oct",
  "nov",
  "dec",
];
export const typoOptions = [
  {
    name: "Intérieur",
    code: "indoor",
    mainCat: [
      {
        name: "Ouvert au public",
        code: "ind-pub",
        categories: [
          { cname: "Centre Commcercial", code: "ip-mall" },
          { cname: "Magasin", code: "ip-shop" },
          { cname: "Centre Tourisme", code: "ip-tourism" },
        ],
      },
      {
        name: "Semi-privé",
        code: "ind-sm",
        categories: [
          { cname: "Mini Golf", code: "ism-mingolf" },
          { cname: "Bowling", code: "ism-mingolf" },
          { cname: "Cinéma", code: "ism-cinema" },
          { cname: "Complèxe Sportif", code: "ism-compsport" },
          { cname: "Salle de sport", code: "ism-sallsport" },
          { cname: "Organisme Formation", code: "ism-formation" },
        ],
      },
    ],
  },
  {
    name: "Extérieur",
    code: "outdoor",
    mainCat: [
      {
        name: "Ouvert au public",
        code: "out-pub",
        categories: [
          {
            name: "Couvert",
            code: "out-pub-couv",
            categories: [
              { cname: "Complexe sportif", code: "opuc-parc" },
              { cname: "Complexe sportif", code: "opuc-parc" },
            ],
          },
          {
            name: "Non Couvert",
            code: "out-pub-out",
            categories: [
              { cname: "Parc", code: "opuo-parc" },
              { cname: "Parc", code: "opuo-parc" },
            ],
          },
        ],
      },
      {
        name: "Semi-privé",
        code: "out-priv",
        categories: [
          {
            name: "Couvert",
            code: "out-priv-couv",
            categories: [
              { cname: "Complexe sportif", code: "oprc-sport" },
              { cname: "Complexe sportif", code: "oprc-sport" },
            ],
          },
          {
            name: "Non Couvert",
            code: "out-priv-out",
            categories: [
              { cname: "Complexe sportif", code: "opro-sport" },
              { cname: "Complexe sportif", code: "opro-sport" },
            ],
          },
        ],
      },
    ],
  },
];
