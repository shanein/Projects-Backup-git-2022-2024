import React from "react";
import { useSelector, useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";

import { Button } from "primereact/button";
import { useEffect, useState, useRef } from "react";
import { api } from "../../services/config";
import { setKiosks } from "../../services/store/kiosksSlice";
import ModifyKiosk from "./ModifyKiosk";
import { SplitButton } from "primereact/splitbutton";
import { Toast } from "primereact/toast";

export default function KioskTable({ setTerminalSelected, setView }) {
  const [showModifySlider, setShowModifySlider] = useState(false);
  const terminals = useSelector((state) => state.kiosks.kiosks);
  const [modifyContent, setModifyContent] = useState({});

  const dispatch = useDispatch();
  const toast = useRef(null);
  const navigate = useNavigate();

  function createItems(terminal) {
    return [
      {
        label: "Informations Update",
        icon: "pi pi-list",
        command: () => {
          setTerminalSelected(terminal);
          setView("terminal");
        },
      },
      {
        label: "Download Installeur",
        icon: "pi pi-download",
        command: async () => {
          await api.get(`/kiosk/${terminal.id}/download`);
        },
      },
      {
        label: "Disable",
        icon: "pi pi-pause",
        command: () => {
          toast.current.show({
            severity: "warn",
            summary: "Kiosk Stopped",
            detail: "Kiosk has been stopped",
          });
        },
      },
      {
        label: "Delete",
        icon: "pi pi-times",
        command: () => {
          toast.current.show({
            severity: "warn",
            summary: "Delete",
            detail: "Data Deleted",
          });
        },
      },
    ];
  }

  return (
    <>
      {terminals &&
        terminals.map((terminal) => (
          <div key={terminal.id} className="flex flex-row align-items-center">
            <div className="flex-1">Active</div>
            <Button
              text
              className="flex-1"
              onClick={() => {
                setTerminalSelected(terminal);
                setView("terminal");
              }}
            >
              <h4>{terminal.name}</h4>
            </Button>
            <div className="flex-1">{terminal.description}</div>
            <div className="flex-1">
              <Button
                icon="pi pi-eraser"
                rounded
                text
                severity="warning"
                aria-label="Notification"
                onClick={() => {
                  setModifyContent(terminal);
                  setShowModifySlider(!showModifySlider);
                }}
              />
              <Button
                icon="pi pi-times"
                rounded
                text
                severity="danger"
                aria-label="Cancel"
              />
            </div>
            <div className="flex-1">
              <SplitButton
                label="Gérer"
                icon="pi pi-sliders-h"
                onClick={() => {
                  setTerminalSelected(terminal);
                  setView("terminal");
                }}
                model={createItems(terminal)}
              />
            </div>
          </div>
        ))}
      <section>
        <ModifyKiosk
          showModifySlider={showModifySlider}
          setShowModifySlider={setShowModifySlider}
          modifyContent={modifyContent}
          setModifyContent={setModifyContent}
        />
      </section>
      <Toast ref={toast} />
    </>
  );
}
