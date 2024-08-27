import React from "react";
import { useNavigate } from "react-router-dom";

export default function OnePage() {
  const navigate = useNavigate();

  return (
    <section className="App">
      <header className="App-header">
        <h1 className="page-title-1">OnePage</h1>
      </header>
      <section id="main-onepage">
        <div>Lorem ipsum</div>
        <div>
          <button onClick={() => navigate("auth")}>Auth</button>
        </div>
      </section>
    </section>
  );
}
