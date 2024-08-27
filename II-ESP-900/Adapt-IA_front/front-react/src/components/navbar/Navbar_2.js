import { Button } from "primereact/button";
import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { useLocation } from "react-router-dom";

import "../../styles/Navbar.scss";
import { apiUrl } from "../../services/config";

const Navbar = () => {
  const user = useSelector((state) => state.auth.user);
  const location = useLocation();
  const [viewActive, setViewActive] = useState("dashboard");
  const navigate = useNavigate();

  useEffect(() => {
    if (location.pathname === "/home") {
      setViewActive("dashboard");
    } else if (
      /^\/kiosk(\/.+)?$/.test(location.pathname) ||
      location.pathname === "/kiosks"
    ) {
      setViewActive("terminals");
    } else if (
      /^\/campaign(\/.+)?$/.test(location.pathname) ||
      location.pathname === "/campaigns"
    ) {
      setViewActive("campaigns");
    } else if (location.pathname === "/account") {
      setViewActive("account");
    } else {
      setViewActive("dashboard");
    }
  }, [location]);

  return (
    <ul style={{ listStyleType: "none", padding: "0 10px", margin: "0" }}>
      <li>
        <Button
          label="Accueil"
          icon="pi pi-th-large"
          onClick={() => {
            setViewActive("dashboard");
            navigate("/home");
          }}
          className={`p-button-text nav-button ${
            viewActive === "dashboard" ? "nav-button-active" : ""
          }`}
          severity="secondary"
        />
      </li>
      {user.user_type == "distributor" || user.is_superuser ? (
        <li>
          <Button
            label="Bornes"
            icon="pi pi-server"
            onClick={() => {
              navigate("/kiosks");
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
      {user.user_type == "advertiser" || user.is_superuser ? (
        <li>
          <Button
            label="Campagnes"
            icon="pi pi-calendar"
            onClick={() => {
              navigate("/campaigns");
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
      {user.is_superuser ? (
        <li>
          <Button
            label="Admin"
            icon="pi pi-shield"
            onClick={() => {
              setViewActive("admin");
              // window.open(`${apiUrl}/admin/`, "_blank");
              window.open(`http://smartdisplay.tech:8081/admin/`, "_blank");
            }}
            className={`p-button-text nav-button ${
              viewActive === "admin" ? "nav-button-active" : ""
            }`}
            severity="secondary"
          />
        </li>
      ) : (
        <></>
      )}
    </ul>
  );
};

export default Navbar;
