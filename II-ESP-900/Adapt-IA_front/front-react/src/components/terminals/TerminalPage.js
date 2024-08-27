
import React, { useState } from "react";
import { useParams } from "react-router-dom";
import Header from "../Header";
import Navbar from "../navbar/Navbar";

// export default function Terminal({ terminal }) {
//   console.log("props", props);
//   return (
//     <div>
//       <div>Terminal Informations Page</div>
//       <div>{terminal.name}</div>
//       <div>{terminal.description}</div>
//       <div>{terminal.localisation}</div>
//       <div>Active : {terminal.is_active}</div>
//     </div>
//   );
// }
export default function TerminalPage() {
  let { id } = useParams();
  const [view, setView] = useState("dashboard");
  const updateView = (value) => {
    setView(value);
  };

  console.log("id", id);

  return (
    <div style={{ height: "100vh", display: "flex", flexDirection: "column" }}>
      <div className={"header-sect"}>
        <Header updateView={updateView} />
      </div>
      <div style={{ flex: "1 1 auto", display: "flex", flexDirection: "row" }}>
        <div className="navbarContainer">
          <Navbar updateView={updateView} />
        </div>
        <div
          style={{
            flex: "1 1 auto",
            backgroundColor: "#f6f6f6",
            borderRadius: "20px 0px 0px 0px",
            padding: "20px",
          }}
          className="pageContainer"
        ></div>
      </div>
    </div>
  );
}
