import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  user: null,
  token: null,
  lastLogin: null,
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    loginUser: (state, action) => {
      state.user = action.payload.user;
      state.token = action.payload.token;
      state.lastLogin = Date.now();
    },
    logoutUser: (state) => {
      state.user = null;
      state.token = null;
      state.lastLogin = null;
    },
    setUser: (state, action) => {
      state.user = action.payload.user;
    },
    setToken: (state, action) => {
      state.token = action.payload.token;
    },
  },
});

export const { loginUser, logoutUser,setUser } = authSlice.actions;
export default authSlice.reducer;
