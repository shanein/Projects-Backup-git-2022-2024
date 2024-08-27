import React, { useEffect, useState } from "react";
import "../../styles/AdPage.scss";
import { Chart } from "primereact/chart";
import ReactPlayer from "react-player";
import { Dropdown } from "primereact/dropdown";
import { Button } from "primereact/button";
import NewCampaign from "./NewCampaign";

import { Card } from "primereact/card";
function AdPage({ ad }) {
  const months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "JUN",
    "JUI",
    "AUG",
    "SEP",
    "OCT",
    "NOV",
    "DEC",
  ];
  const created = convertDate(ad.start_date);
  const [chartData, setChartData] = useState({});
  const [chartOptions, setChartOptions] = useState({});
  const [selectedCity, setSelectedCity] = useState(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const cities = [
    { name: "New York", code: "NY" },
    { name: "Rome", code: "RM" },
    { name: "London", code: "LDN" },
    { name: "Istanbul", code: "IST" },
    { name: "Paris", code: "PRS" },
  ];

  function convertDate(dateString) {
    const date = new Date(dateString);

    return (
      date.getDate() +
      " " +
      months[date.getMonth() + 1] +
      " " +
      date.getFullYear() +
      " " +
      date.getHours() +
      ":" +
      date.getMinutes() +
      ":" +
      date.getSeconds()
    );
  }

  useEffect(() => {
    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue("--text-color");
    const textColorSecondary = documentStyle.getPropertyValue(
      "--text-color-secondary"
    );
    const surfaceBorder = documentStyle.getPropertyValue("--surface-border");
    const data = {
      labels: ["January", "February", "March", "April", "May", "June", "July"],
      datasets: [
        {
          label: "First Dataset",
          data: [65, 59, 80, 81, 56, 55, 40],
          fill: false,
          borderColor: documentStyle.getPropertyValue("--blue-500"),
          tension: 0.4,
        },
        {
          label: "Second Dataset",
          data: [28, 48, 40, 19, 86, 27, 90],
          fill: false,
          borderColor: documentStyle.getPropertyValue("--pink-500"),
          tension: 0.4,
        },
      ],
    };
    const options = {
      maintainAspectRatio: false,
      aspectRatio: 0.6,
      plugins: {
        legend: {
          labels: {
            color: textColor,
          },
        },
      },
      scales: {
        x: {
          ticks: {
            color: textColorSecondary,
          },
          grid: {
            color: surfaceBorder,
          },
        },
        y: {
          ticks: {
            color: textColorSecondary,
          },
          grid: {
            color: surfaceBorder,
          },
        },
      },
    };

    setChartData(data);
    setChartOptions(options);
  }, []);
  return (
    <div>
      <div className="campaign">
        <div className="flex bloc">
          <div className="grid ">
            <div className="col  ">
              <div className="grid">
                <div className="col">
                  <ul className="text-right list-none p-0">
                    <li className="bloc-title">Campaign ID</li>
                    <li className="bloc-title">Created at</li>
                    <li className="bloc-title">Geo. area</li>
                    <li className="bloc-title">Area</li>
                  </ul>
                </div>
                <div className="col">
                  <ul className="text-left list-none p-0 ">
                    <li className="bloc-value camp-info">{ad.id}</li>
                    <li className="bloc-value">{created}</li>
                    <li className="bloc-value camp-info">{ad.address}</li>
                    <li className="bloc-value camp-info">{ad.address}</li>
                  </ul>
                </div>
                <div className="col flex justify-between items-center">
                  <div className="stats m-2">
                    <div className="text-center">
                      <span className="pi pi-megaphone text-3xl py-3"></span>
                    </div>
                    <div className="text-center bg-white btm">
                      <span className="bloc-title">85 %</span>
                    </div>
                  </div>
                  <div className="stats m-2">
                    <div className="text-center">
                      <span className="pi pi-users  text-3xl px-2 py-3"></span>
                    </div>
                    <div className="text-center bg-white btm">
                      <span className="bloc-title">500 views</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        {!ad.is_active && (
          <div className="grid justify-end">
            <Button
              icon="pi pi-ban"
              severity="warning"
              label="Continuer la création de l'annonce"
              onClick={() => {
                // Action à effectuer lors du clic sur le bouton
                setShowCreateModal(true);
              }}
            />

          <div>
       {showCreateModal ?  <NewCampaign
          showCreateModal={showCreateModal}
          setShowCreateModal={setShowCreateModal}
          campaign={ad}
        /> : <></>}
      </div>
          </div>
        )}
      </div>
      <div className="grid">
        <div className="col bloc ">
          <span className="bloc-title">Description</span>
          <p className="text-600 p-2">{ad.description}</p>
        </div>
        <div className="col h-auto flex items-center justify-center ">
          <div
            className=" camp-date-border text-center m-auto p-2 border-1 border-round border-round-2xl"
            style={{ backgroundColor: "white" }}
          >
            <span className="font-bold text-sm">
              {new Date(ad.start_date).toLocaleString()}
            </span>
            <i className="pi pi-arrow-right mx-2 text-xs"></i>
            <span className="font-bold text-sm">
              {new Date(ad.end_date).toLocaleString()}
            </span>
          </div>
        </div>
      </div>
      <div className="grid">
        <div className="col bloc mr-2 text-center">
          <span className="bloc-title">Remaining budget</span>
          <p className="descText">
            <span className="remaining-budget">{ad.budget} €</span>
          </p>
        </div>
        <div className="col bloc ml-2">
          <span className="bloc-title">Targets</span>
          <div className="grid">
            <div className="col">
              <span className="target-age-gender">Age</span>
              <p>Children (0-12 years)</p>
            </div>
            <div className="col">
              <span className="target-age-gender">Gender</span>
              <p>Males-Females</p>
            </div>
          </div>
          <div className="card flex justify-content-end">
            <span className="p-float-label">
              <Dropdown
                inputId="dd-city"
                value={selectedCity}
                onChange={(e) => setSelectedCity(e.value)}
                options={cities}
                optionLabel="name"
                className="w-full border-0 bg-transparent"
              />
              <label htmlFor="dd-city">Plus</label>
            </span>
          </div>
        </div>
      </div>
      <div className="grid mt-4">
        <div className="col">
          <ReactPlayer
            url={ad.videoUrl}
            width="6O%"
            height="100%"
            controls
            style={{
              aspectRatio: 1080 / 1920,
              maxHeight: "300px",
              margin: "auto",
            }}
          />
        </div>
        <div className="col">
          <Chart
            type="line"
            data={chartData}
            options={chartOptions}
            width="488"
            height="300"
          />
        </div>
      </div>
    </div>
  );
  
}

export default AdPage;
