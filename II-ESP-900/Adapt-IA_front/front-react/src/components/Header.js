// import React from 'react'
import Logo from "./shared/Logo";
import React, { useState } from "react";
import { AutoComplete, InputText, Avatar, Badge } from "primereact";
import "../styles/header.scss";
// import Logo from "../assets/logo_smart-display.png";
import Hibou from "../assets/logo_smart-display_hibou.png";
import { logoutUser } from "../services/store/authSlice";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { Button } from "primereact/button";

export default function Header() {
  let count = 0;
  const [notifs, setNotifs] = useState(1);
  const [userNotifs, setUserNotifs] = useState(2);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  // const biggerSearch = () => {
  //   count === 0
  //     ? (document.getElementById("searchB").classList.toggle("p-inputtext-sm"),
  //       count++)
  //     : // <></>
  //       null;
  // };
  return (
    <section id="header-section">
      <div className="header-logo-blc">
        {/*<Logo width={50} height={50} />*/}
        <Logo width={162} height={44} />
        {/*SMART DISPLAY{" "}*/}
      </div>
      <div className="card flex justify-content-center">
        {/* <AutoComplete
          value={value}
          suggestions={items}
          completeMethod={search}
          onChange={(e) => setValue(e.value)}
        /> */}
        {/* <span className="p-input-icon-left">
          <i className="pi pi-search" />
          <InputText
            id="searchB"
            placeholder="Search"
            className="p-inputtext-sm"
            onClick={biggerSearch}
          />
        </span> */}
      </div>
      <div className="iconsList">
        {/* <span>
          {notifs > 0 ? (
            <Badge className="notif-badge" value={notifs} severity="danger" />
          ) : (
            <></>
          )}
          <Avatar icon="pi pi-bell" size="large"></Avatar>
        </span> */}
        {/* <span
          onClick={() => navigate("/account")}
          style={{ cursor: "pointer" }}
        >
          {userNotifs > 0 ? (
            <Badge
              className="avatar-badge"
              value={userNotifs}
              severity="danger"
            />
          ) : (
            <></>
          )}
          <Avatar icon="pi pi-user" size="large"></Avatar>
        </span> */}

        <Button
          onClick={() => navigate("/account")}
          style={{ cursor: "pointer" }}
          icon="pi pi-user"
          className="m-0 prof-btn"
          text
          rounded
          color="white"
          size="large"
        />
      </div>
    </section>
  );
}
