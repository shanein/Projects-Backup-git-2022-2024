import React, { useEffect, useState, useRef } from "react";
import { api } from "../services/config";
import { Button } from "primereact/button";
import { Dialog } from "primereact/dialog";
import NewKiosk from "./terminals/NewKiosk";
import ModifyKiosk from "./terminals/ModifyKiosk";
import { useSelector } from "react-redux";
import { useDispatch } from "react-redux";
import { setKiosks } from "../services/store/kiosksSlice";
import { Toast } from "primereact/toast";
import KioskTable from "./terminals/KioskTable";
import KioskTable2 from "./terminals/KioskTable_2";
import TerminalPage from "./terminals/TerminalPage";
import TerminalPage2 from "./terminals/TerminalPage_2";

export default function Terminals() {
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showModifySlider, setShowModifySlider] = useState(false);
  const terminals = useSelector((state) => state.kiosks.kiosks);
  const [modifyContent, setModifyContent] = useState({});
  const [terminalSelected, setTerminalSelected] = useState({});

  const [view, setView] = useState("terminals");
  const updateView = (value) => {
    setView(value);
  };

  const [disableScroll, setDisableScroll] = useState(false);

  const dispatch = useDispatch();
  const toast = useRef(null);

  useEffect(() => {
    const terminals = async () => {
      try {
        const resp = await api.get("/terminal");
        dispatch(setKiosks(resp.data));
      } catch (error) {
        console.error(error);
        toast.current.show({
          severity: "error",
          summary: "Error",
          detail: "Error while fetching terminals",
          life: 3000,
        });
      }
    };
    terminals();
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
    <main id="terminal-main" className="pages-main">
      <h1>Terminals</h1>
      <div className="newActionBtnR2" id="newKioskDiv">
        {view === "terminals" ? (
          <Button
            icon="pi pi-plus"
            label="New Kiosk"
            onClick={() => {
              setShowCreateModal(true);
              setDisableScroll(true);
            }}
          />
        ) : (
          <></>
        )}
      </div>
      {view === "terminals" ? (
        <section className="m-5">
          <KioskTable2
            setTerminalSelected={setTerminalSelected}
            setView={updateView}
          />
        </section>
      ) : (
        <></>
      )}

      <section>
        <ModifyKiosk
          showModifySlider={showModifySlider}
          setShowModifySlider={(value) => {
            setShowModifySlider(value);
            setDisableScroll(false); // Réactiver le défilement lors de la fermeture de la popup
          }}
          modifyContent={modifyContent}
          setModifyContent={setModifyContent}
        />
      </section>

      <section>
        <NewKiosk
          showCreateModal={showCreateModal}
          setShowCreateModal={(value) => {
            setShowCreateModal(value);
            setDisableScroll(false); // Réactiver le défilement lors de la fermeture de la popup
          }}
        />
      </section>

      <section>
        {view !== "terminals" ? (
          <div className="returnBtnLeft" id="newKioskDiv">
            <Button
              icon="pi pi-arrow-left"
              severity="warning"
              label="Retour"
              onClick={() => setView("terminals")}
            />
          </div>
        ) : (
          <></>
        )}
      </section>
      {view === "terminal" && terminalSelected ? (
        <section>
          <TerminalPage2 terminal={terminalSelected} />
        </section>
      ) : (
        <></>
      )}
      <Toast ref={toast} />
    </main>
  );
}
