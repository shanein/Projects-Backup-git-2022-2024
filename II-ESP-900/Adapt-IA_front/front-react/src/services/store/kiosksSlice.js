import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  kiosks: [],
};

const kiosksSlice = createSlice({
  name: "kiosks",
  initialState,
  reducers: {
    setKiosks: (state, action) => {
      // state.kiosks = action.payload.kiosks;
      state.kiosks = action.payload;
    },
    cleanKiosks: (state) => {
      state.kiosks = [];
    },
    addKiosk: (state, action) => {
      // state.kiosks.push(action.payload.kiosk);
      state.kiosks.push(action.payload);
    },
    updateKiosk: (state, action) => {
      const updateKiosk = state.kiosks.map(ter => {
        if (ter.id === action.payload.id) {
          return action.payload;
        }
        return ter;
      });
      state.kiosks = updateKiosk;
    }
  },
});

export const { setKiosks, cleanKiosks, addKiosk , updateKiosk} = kiosksSlice.actions;
export default kiosksSlice.reducer;
