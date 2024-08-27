import React from "react";
import Header from "../components/Header";
import Navbar from "../components/navbar/Navbar";
import Navbar2 from "../components/navbar/Navbar_2";
import "../styles/Home.scss";

export default function Generic({ component }) {
  const NavbarWidth = () => {
    return document.getElementById("navbarContainer").offsetWidth;
  };

  return (
    <div
      style={{
        height: "100vh",
        maxWidth: "100vw",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <div className={"header-sect"}>
        <Header />
      </div>
      <div style={{ flex: "1 1 auto", display: "flex", flexDirection: "row" }}>
        <div className="navbarContainer" style={{ maxWidth: "188px" }}>
          <Navbar2 />
        </div>
        <div
          style={{
            flex: "1 1 auto",
            backgroundColor: "#f6f6f6",
            borderRadius: "20px 0px 0px 0px",
            padding: "20px",
            maxWidth: `calc(100vw - ${NavbarWidth}px)`,
            width: "-webkit-fill-available",
          }}
          className="pageContainer"
        >
          {component}
        </div>
      </div>
    </div>
  );
}
