import React, { useState } from "react";
import Profile from "./account/Profile";
import BankInfos from "./account/BankInfos";
import { Button } from "primereact/button";
import { useDispatch } from "react-redux";
import { logoutUser } from "../services/store/authSlice";

export default function Account() {
  const dispatch = useDispatch();
  const [show, setShow] = useState("home");

  return (
    <main id="account-main" className="pages-main">
      <h1>Mon Compte</h1>
      <section className="accountContent flex flex-column align-items-center justify-content-center">
        {show === "home" ? (
          <>
            <div>
              <Button
                label="Mon Profile"
                className="m-5"
                onClick={() => setShow("profile")}
              />
            </div>
            {/* <Button
              label="Mes informations bancaires"
              className="m-5"
              onClick={() => setShow("bank")}
            /> */}
            <div>
              <Button
                label="Déconnexion"
                className="p-button-danger m-5"
                onClick={() => dispatch(logoutUser())}
              />
            </div>
          </>
        ) : (
          <div className="returnBtnLeft" id="newKioskDiv">
            <Button
              icon="pi pi-arrow-left"
              severity="warning"
              label="Retour"
              onClick={() => setShow("home")}
            />
          </div>
        )}
        {show === "profile" ? <Profile /> : <></>}
        {/* {show === "bank" ? <BankInfos /> : <></>} */}
      </section>
    </main>
  );
}
