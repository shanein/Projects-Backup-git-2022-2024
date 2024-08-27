import React from "react";
import logo from "../../assets/logo_sd.png";
import { useNavigate } from "react-router-dom";

export default function Logo({ width, height }) {
  const navigate = useNavigate();
  return (
    <div>
      <img
        src={logo}
        alt="logo"
        width={width}
        height={height}
        onClick={() => navigate("/home")}
        className="logoAuth"
      />
    </div>
  );
}
