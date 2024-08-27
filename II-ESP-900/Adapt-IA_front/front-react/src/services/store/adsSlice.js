import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  ads: [],
};

const adsSlice = createSlice({
  name: "ads",
  initialState,
  reducers: {
    setAds: (state, action) => {
      state.ads = action.payload;
    },
    cleanAds: (state) => {
      state.ads = [];
    },
    addAds: (state, action) => {
      state.ads.push(action.payload);
    },
    removeAds: (state, action) => {
      state.ads = state.ads.filter((ad) => ad.id !== action.payload.id);
    },
    updateAds: (state, action) => {
      const updatedAds = state.ads.map(ad => {
        if (ad.id === action.payload.id) {
          return action.payload;
        }
        return ad;
      });
      state.ads = updatedAds;
    },

    deleteVideoUrl: (state, action) => {
      // supprimer l'url de la vidéo de l'annonce correspondante et renvoyer la liste des annonces
      const updatedAds = state.ads.map(ad => {
        if (ad.videoUrl === action.payload) {
          ad.videoUrl = null;
        }
        return ad;
      });
      state.ads = updatedAds;
    },
  },
});

export const { setAds, cleanAds, addAds, removeAds, updateAds, deleteVideoUrl } = adsSlice.actions;

export default adsSlice.reducer;
