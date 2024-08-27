import React from "react";
import { Button } from "primereact/button";

export default function Dashboard() {
  return (
    <main id="dashboard-main" className="pages-main">
      <h1>Dashboard</h1>
      <div className="newActionBtnR2">
        {/* <Button label="New" icon="pi pi-plus" className="p-button-info" /> */}
      </div>
      <section className="dashboardContent"></section>
    </main>
  );
}
