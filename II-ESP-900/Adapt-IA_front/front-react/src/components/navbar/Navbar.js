import { Button } from "primereact/button";
import React, { useState } from "react";
import { useSelector } from "react-redux";

import "../../styles/Navbar.scss";

const Navbar = ({ updateView }) => {
  const user = useSelector((state) => state.auth.user);

  const [viewActive, setViewActive] = useState("dashboard");

  return (
    <ul style={{ listStyleType: "none", margin: "0" }}>
      <li>
        <Button
          label="Accueil"
          icon="pi pi-th-large"
          onClick={() => {
            updateView("dashboard");
            setViewActive("dashboard");
          }}
          className={`p-button-text nav-button ${
            viewActive === "dashboard" ? "nav-button-active" : ""
          }`}
          severity="secondary"
        />
      </li>
      {user.user_type == "distributor" ? (
        <li>
          <Button
            label="Bornes"
            icon="pi pi-server"
            onClick={() => {
              updateView("terminals");
              setViewActive("terminals");
            }}
            className={`p-button-text nav-button ${
              viewActive === "terminals" ? "nav-button-active" : ""
            }`}
            severity="secondary"
          />
        </li>
      ) : (
        <></>
      )}
      {user.user_type == "advertiser" ? (
        <li>
          <Button
            label="Campagnes"
            icon="pi pi-calendar"
            onClick={() => {
              updateView("campaigns");
              setViewActive("campaigns");
            }}
            className={`p-button-text nav-button ${
              viewActive === "campaigns" ? "nav-button-active" : ""
            }`}
            severity="secondary"
          />
        </li>
      ) : (
        <></>
      )}
      {/* {user.is_superuser ? ( */}
      <li>
        <Button
          label="Admin"
          icon="pi pi-shield"
          onClick={() => {
            updateView("admin");
            setViewActive("admin");
          }}
          className={`p-button-text nav-button ${
            viewActive === "admin" ? "nav-button-active" : ""
          }`}
          severity="secondary"
        />
      </li>
      {/* ) : (
        <></>
      )} */}
    </ul>
  );
};

export default Navbar;
