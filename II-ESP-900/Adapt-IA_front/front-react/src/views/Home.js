import React, { Suspense, lazy, useEffect, useState } from "react";
import Navbar from "../components/navbar/Navbar";
// import Header from "../components/Header";
import "../styles/Home.scss";
import { ProgressSpinner } from "primereact/progressspinner";
// import Navbar2 from "../components/navbar/Navbar_2";

const Dashboard = lazy(() => import("../components/Dashboard"));
const Terminals = lazy(() => import("../components/Terminals"));
const Terminals2 = lazy(() => import("../components/Terminals_2"));
const Campaigns = lazy(() => import("../components/Campaigns"));
const Account = lazy(() => import("../components/Account"));
// const Terminal = lazy(() => import("../components/terminals/TerminalPage"));
const Navbar2 = lazy(() => import("../components/navbar/Navbar_2"));
const Header = lazy(() => import("../components/Header"));

export default function Home() {
  const [view, setView] = useState("dashboard");
  const updateView = (value) => {
    setView(value);
  };

  return (
    <div style={{ height: "100vh", display: "flex", flexDirection: "column" }}>
      <div className={"header-sect"}>
        <Header updateView={updateView} />
      </div>
      <div style={{ flex: "1 1 auto", display: "flex", flexDirection: "row" }}>
        <div className="navbarContainer">
          {/* <Navbar updateView={updateView} /> */}
          <Navbar2 />
        </div>
        <div
          style={{
            flex: "1 1 auto",
            backgroundColor: "#f6f6f6",
            borderRadius: "20px 0px 0px 0px",
            padding: "20px",
          }}
          className="pageContainer"
        >
          <Suspense fallback={<ProgressSpinner />}>
            {
              {
                dashboard: <Dashboard />,
                // terminals: <Terminals />,
                terminals: <Terminals2 />,
                campaigns: <Campaigns />,
                account: <Account />,
              }[view]
            }
          </Suspense>
        </div>
      </div>
    </div>
  );
}
