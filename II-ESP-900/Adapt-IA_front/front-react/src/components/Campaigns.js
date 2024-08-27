import React, { useEffect, useState } from "react";
import { Button } from "primereact/button";

import { api } from "../services/config";
import NewCampaign from "./campaigns/NewCampaign";
import CampaignsTable from "./campaigns/CampaignsTable";
import { useDispatch } from "react-redux";
import { setAds } from "../services/store/adsSlice";
import AdPage from "./campaigns/AdPage";

export default function Campaigns() {
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [adSelected, setAdSelected] = useState({});
  const [view, setView] = useState("ads");
  const [campaigns, setCampaigns] = useState({});
  const updateView = (value) => {
    setView(value);
  };
  const dispatch = useDispatch();

  const [disableScroll, setDisableScroll] = useState(false);

  useEffect(() => {
    const campaigns = async () => {
      try {
        const resp = await api.get("/campaigns/");
        dispatch(setAds(resp.data));
        setCampaigns(resp.data);

      
      } catch (error) {
        console.error(error);
      }
    };
    campaigns();
  }, []);

  // Fonction pour activer ou désactiver le scroll
  useEffect(() => {
    if (disableScroll) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "auto";
    }
  }, [disableScroll]);

  return (
    <main id="campaigns-main" className="pages-main">
      {view === "ads" ? <h1>Annonces</h1> : <h1>{adSelected.name}</h1>}

     
      <div className="newActionBtnR2" id="newCampaginDiv">
        {view === "ads" ? (
          <Button
            icon="pi pi-plus"
            label="New Campaign"
            // onClick={() => setShowCreateModal(true)}
            onClick={() => {
              setShowCreateModal(true);
              setDisableScroll(true);
            }}
          />
        ) : (
          <></>
        )}
      </div>
      <section>
        {view !== "ads" ? (
          <div className="returnBtnLeft" id="newKioskDiv">
            <Button
              label="Modifier"
              severity="secondary"
              className={"mr-4"}
              raised
              outlined
            />
            <Button
              icon="pi pi-arrow-left"
              severity="warning"
              label="Retour"
              onClick={() => setView("ads")}
            />
          </div>
          
        ) : (
          <></>
        )}
      </section>
      {/* {view === "new" ? ( */}
      <section>
        <NewCampaign
          showCreateModal={showCreateModal}
          setShowCreateModal={(value) => {
            setShowCreateModal(value);
            setDisableScroll(false); // Réactiver le défilement lors de la fermeture de la popup
          }}
          campaign={{}}
          setCampaigns={setCampaigns}
        />
      </section>
      {/* ) : (
        <></>
      )} */}
      {view === "ad" ? (
        <section>
          <AdPage
            // showCreateModal={showCreateModal}
            // setShowCreateModal={setShowCreateModal}
            ad={adSelected}
          />
        </section>
      ) : (
        <></>
      )}
      {view === "ads" ? (
        <section>
          <CampaignsTable setAdSelected={setAdSelected} setView={updateView} />
        </section>
      ) : (
        <></>
      )}
    </main>
  );
}
