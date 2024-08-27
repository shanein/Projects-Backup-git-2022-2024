import { configureStore } from "@reduxjs/toolkit";
import { combineReducers } from "redux";
import {
  persistReducer,
  persistStore,
  FLUSH,
  REHYDRATE,
  PAUSE,
  PERSIST,
  PURGE,
  REGISTER,
} from "redux-persist";
import storage from "redux-persist/lib/storage";
import authReducer from "./authSlice";
import kiosksReducer from "./kiosksSlice";
import adsReducer from "./adsSlice";

const rootReducer = combineReducers({
  auth: authReducer,
  kiosks: kiosksReducer,
  ads: adsReducer,
});

const persistConfig = {
  key: "root",
  storage,
  whitelist: ["auth", "kiosks", "ads"], // authReducer sera persisté
};

const persistedReducer = persistReducer(persistConfig, rootReducer);

const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
      },
    }),
});

export const persistor = persistStore(store);
export default store;
