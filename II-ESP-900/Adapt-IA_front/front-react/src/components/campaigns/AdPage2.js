import React, { useEffect, useState, useRef } from "react";
import "../../styles/AdPage.scss";
import { Chart } from "primereact/chart";
import ReactPlayer from "react-player";
import { Dropdown } from "primereact/dropdown";
import { useParams } from "react-router-dom";
import { useSelector } from "react-redux";
import { Button } from "primereact/button";
import { useNavigate } from "react-router-dom";
import NewCampaign from "./NewCampaign";
import { apiService } from "../../services/ApiService";
import { useDispatch } from "react-redux";
import { updateAds } from "../../services/store/adsSlice";
import { InputText } from "primereact/inputtext";
import { InputTextarea } from "primereact/inputtextarea";
import { Toast } from 'primereact/toast';

function AdPage({ ad }) {
  let { id } = useParams();
  const dispatch = useDispatch();
  const [adSelected, setAdSelected] = useState(null);
  const campaigns = useSelector((state) => state.ads.ads);
  const [is_active, setIs_active] = useState(false);
  const [is_valid, setIs_valid] = useState(false);
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
  const [created, setCreated] = useState(null);
  const [chartData, setChartData] = useState({});
  const [chartOptions, setChartOptions] = useState({});
  const [selectedCity, setSelectedCity] = useState(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [modif, setModif] = useState(false);

  const [editedName, setEditedName] = useState(adSelected && adSelected.name);
  const [editedDescription, setEditedDescription] = useState(adSelected && adSelected.description);
  const [editedBudget, setEditedBudget] = useState(adSelected && adSelected.budget || 0);
  const toast = useRef(null);
  const cities = [
    { name: "New York", code: "NY" },
    { name: "Rome", code: "RM" },
    { name: "London", code: "LDN" },
    { name: "Istanbul", code: "IST" },
    { name: "Paris", code: "PRS" },
  ];

  const navigate = useNavigate();

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
    if (id) {
      setAdSelected(campaigns.find((camp) => camp.id == id));
    }
  }, [id, campaigns]);

  useEffect(() => {
    if (ad) {
      setAdSelected(ad);
      setIs_active(ad.is_active);
      setIs_valid(ad.is_valid);
    }
  }, []);

  useEffect(() => {
    if (adSelected) {
    
      setCreated(convertDate(adSelected.start_date));
      setIs_active(adSelected.is_active);
      setIs_valid(adSelected.is_valid);
    }
  }, [adSelected]);
  
  useEffect(() => {

  }, [adSelected, is_active, is_valid]);

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

  const handleClick = () => {
    if (adSelected.is_valid) {
      setModif(!modif);
      if (!modif) {
        setEditedName(adSelected.name);
        setEditedDescription(adSelected.description);
        setEditedBudget(adSelected.budget);
      } 
    }else{
      console.log("Campaign is not valid, you can't edit it.");
   
  }
  };
  const handleInputChangeName = (e) => {
    setEditedName(e.target.value);

  };

  const handleInputChangeDescription = (e) => {
    setEditedDescription(e.target.value);

  };

  const handleEditClick = () => {
    setModif(true);

  };

  const addBugetClick = (add) => {
    setEditedBudget(editedBudget + add);
  }

  const UpdateCampaign = (name , description, budget) => {
    apiService.updateCampaign(adSelected.id, name, description, budget, adSelected.is_smart).then((response) => {
      setAdSelected(response.data);
      dispatch(updateAds(response.data))
      setModif(false);
    
    }
    );
  }

 
  

  return (
    <div
      style={{
        flex: "1 1 auto",
        backgroundColor: "#f6f6f6",
        borderRadius: "20px 0px 0px 0px",
        padding: "20px",
      }}
      className="pageContainer"
    >
      <div> 
   
      {modif ? (
  <>
<div className="flex" style={{ alignItems: 'center' }}>
  <h1 style={{ marginBottom: '0', fontSize: '1.5rem' }}>Campaign : </h1>
  <InputText
    type="text"
    value={editedName}
    onChange={handleInputChangeName}
    placeholder="Nom de la campagne"
  />
</div>
  </>
) : (
  <h1 onClick={handleEditClick}>Campaign : {adSelected && adSelected.name}</h1>
)}

        <section>
 
        <div className="returnBtnLeft" id="newKioskDiv">

  
  <div className="flex">
    {modif ? (
      <>
     
        <Button
          icon="pi pi-check"
          label="Valider"
          onClick={() => UpdateCampaign(editedName, editedDescription, editedBudget)}
          severity="success"
          className="mr-4"
          raised
          outlined
        />
           <Toast ref={toast} />
        <Button
          icon="pi pi-times"
          label="Annuler"
          onClick={handleClick}
          severity="danger"
          className="mr-4"
          raised
          outlined
        />
      </>
      
    ) : (
      <>
        {is_active && is_valid ? (
          <Button
            label="Modifier"
            onClick={handleClick}
            severity="secondary"
            icon="pi pi-pencil"
            className="mr-4"
            raised
            outlined
          />
        ) : !is_active ? (
          <Button
            label="Continuer la création de l'annonce"
            onClick={() => setShowCreateModal(true)}
            severity="warning"
            icon="pi pi-pencil"
            className="mr-4"
            raised
            outlined
          />
        ) : null}
      </>
    )}

    {showCreateModal && (
      <NewCampaign
        showCreateModal={showCreateModal}
        setShowCreateModal={setShowCreateModal}
        campaign={adSelected}
        setAtSelected={setAdSelected}
      />
    )}

    <Button
      icon="pi pi-arrow-left"
      severity="warning"
      label="Retour"
      onClick={() => navigate("/campaigns")}
      raised
      outlined
    />
  </div>
</div>

</section>
        <>
          {adSelected && (
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
                          <li className="bloc-title"> Area</li>
                        </ul>
                      </div>
                      <div className="col">
                        <ul className="text-left list-none p-0 ">
                          <li className="bloc-value camp-info">
                            {adSelected.id}
                          </li>
                          <li className="bloc-value">{created}</li>
                          <li className="bloc-value camp-info">
                            {adSelected.address}
                          </li>
                          <li className="bloc-value camp-info">
                            {adSelected.address}
                          </li>
                        </ul>
                      </div>
                      <div className="col flex ">
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
            
              <div className="grid">
              <div className="col bloc">
      <span className="bloc-title">Description</span>
      <br /> {/* Ajout d'un saut de ligne pour placer l'input en dessous */}
      {modif ? (
        <InputTextarea
          id="camp-description"
          type="text"
          value={editedDescription}
          onChange={handleInputChangeDescription}
          placeholder="Description de la campagne"
          className="input-description" // Appliquez la classe CSS
        />
      ) : (
        <p className="text-600 p-2">{adSelected.description}</p>
      )}
           </div>
                <div className="col h-auto flex items-center justify-center ">
                  <div
                    className=" camp-date-border text-center m-auto p-2 border-1 border-round border-round-2xl"
                    style={{ backgroundColor: "white" }}
                  >
                    <span className="font-bold text-sm">
                      {new Date(adSelected.start_date).toLocaleString()}
                    </span>
                    <i className="pi pi-arrow-right mx-2 text-xs"></i>
                    <span className="font-bold text-sm">
                      {new Date(adSelected.end_date).toLocaleString()}
                    </span>
                  </div>
                </div>
              </div>

              <div className="grid">
                <div className="col bloc mr-2 text-center">
                  <span className="bloc-title">Crédits restants</span>
                  <p className="descText">
                      <span className="remaining-budget">
                        {!modif ? adSelected.budget : editedBudget} €
                      </span>
                      <br /> {/* Ajout d'un saut de ligne pour placer les boutons en dessous du texte */}
                      {modif ? (
                        <span className="p-buttonset">
                        <Button label="+10" onClick={() => addBugetClick(10)} />
                        &nbsp; {/* Ajoute un espace */}
                        <Button label="+20" onClick={() => addBugetClick(20)} />
                        &nbsp; {/* Ajoute un espace */}
                        <Button label="+50" onClick={() => addBugetClick(50)} />
                      </span>
                      ) : null}
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
                    url={adSelected.videoUrl || adSelected.video_url}
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
          )}
        </>
      </div>
    </div>
  );
}

export default AdPage;
