import React, { useCallback, useEffect, useRef, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

import CustomToast from "../shared/CustomToast";
import "../../styles/AdPage.scss";
import Header from "../Header";
import Navbar from "../navbar/Navbar";
import { Button } from "primereact/button";
import { useSelector } from "react-redux";
import { useDispatch } from "react-redux";

import { Terminal } from "primereact/terminal";

import { InputSwitch } from "primereact/inputswitch";
import { sanitizeInput } from "../../services/utils";
import axios from "axios";
import _ from "lodash";
import { AutoComplete } from "primereact/autocomplete";
import { findAllByDisplayValue } from "@testing-library/react";
import { ListBox } from "primereact/listbox";
import { CascadeSelect } from "primereact/cascadeselect";
import { Calendar } from "primereact/calendar";
import { typoOptions } from "../../services/utils";
import { Dialog } from "primereact/dialog";
import ReactDOM from "react-dom/client";
import { api } from "../../services/config";
import {
  addKiosk,
  setKiosks,
  updateKiosk,
} from "../../services/store/kiosksSlice";
import { Toast } from "primereact/toast";

export default function TerminalPage({ terminal }) {
  let { id } = useParams();
  const terminals = useSelector((state) => state.kiosks.kiosks);
  const navigate = useNavigate();
  const [terminalData, setTerminalData] = useState(null);
  const [selectedTypology, setSelectedTypology] = useState(null);
  const [showError, setShowError] = useState(false);
  const [planning, setPlanning] = useState([]);
  const days = [
    "lundi",
    "mardi",
    "mercredi",
    "jeudi",
    "vendredi",
    "samedi",
    "dimanche",
  ];
  const today = new Date();
  const calendarRef = React.createRef();
  const toast = useRef(null);
  const [address, setPlace] = useState("");
  const nextDay = new Date();
  const [view, setView] = useState("dashboard");
  const [places, setPlaces] = useState([]);
  const [checked, setChecked] = useState(true);

  const [visible, setVisible] = useState(false);
  const [visibleUn, setVisibleUn] = useState(false);
  const [selectedUnavailableDate, setSelectedUnavailableDate] = useState(null);
  const [unavailableDates, setUnavailableDates] = useState([]);
  const [dates, setViewDate] = useState([]);
  const [SelectedDates, setDates] = useState([]);

  // unavailable date list actions
  const [editing, setEditing] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [updating, setUpdating] = useState(false);

  const [showToast, setshowToast] = useState(false);
  const [showWarn, setShowWarn] = useState(false);
  const [isEditingTypology, setIsEditingTypology] = useState(false); // État pour contrôler le mode d'édition
  const [isEditingName, setIsEditingName] = useState(false); // État pour contrôler le mode d'édition
  const [isEditingDescription, setIsEditingDescription] = useState(false); // État pour contrôler le mode d'édition
  const [name, setName] = useState(""); // L'état initial sera défini lors du chargement des données
  const [description, setDescription] = useState("");

  useEffect(() => {
    if (id) {
      setTerminalData(terminals.find((term) => term.id === id));
    }
  }, [id, terminals]);
  useEffect(() => {
    if (terminal) {
      setTerminalData(terminal);
    }
  }, [terminal]);
  useEffect(() => {
    if (terminalData) {
      prepareData();
    }
  }, [terminalData]);

  useEffect(() => {
    setTimeout(() => {
      setShowError(false);
    }, 5000);
  }, [showError]);
  useEffect(() => {
    setTimeout(() => {
      setShowWarn(false);
    }, 5000);
  }, [showWarn]);

  useEffect(() => {
    if (terminalData) {
      setName(terminalData.name);
      setDescription(terminalData.description);
      setSelectedTypology(terminalData.place_type);
      // console.log(findCNameByCode(terminalData.place_type))
      setSelectedTypology(findCNameByCode(terminalData.place_type));
    }
  }, [terminalData]);

  function convertDate(dateString) {
    const tmp = new Date(dateString);
    const months = [
      "Jan",
      "Fev",
      "Mar",
      "Avr",
      "Mai",
      "Jui",
      "Jul",
      "Aoû",
      "Sep",
      "Oct",
      "Nov",
      "Déc",
    ];
    return (
      tmp.getDate() + " " + months[tmp.getMonth()] + " " + tmp.getFullYear()
    );
  }

  const codeToCNameMap = [
    { code: "ip-mall", cname: "Centre Commercial" },
    { code: "ip-shop", cname: "Magasin" },
    { code: "ip-tourism", cname: "Centre Tourisme" },
    { code: "ism-mingolf", cname: "Mini Golf" }, // Notez qu'il y a une erreur dans votre structure originale, 'ism-mingolf' apparaît deux fois avec des valeurs différentes. Ajustez selon le besoin réel.
    { code: "ism-bowling", cname: "Bowling" }, // Correction assumée pour la duplication de 'ism-mingolf'
    { code: "ism-cinema", cname: "Cinéma" },
    { code: "ism-compsport", cname: "Complèxe Sportif" },
    { code: "ism-sallsport", cname: "Salle de sport" },
    { code: "ism-formation", cname: "Organisme Formation" },
    { code: "opuc-parc", cname: "Complexe sportif" }, // Ajustez si 'Complexe sportif' sous 'Couvert' a un cname différent
    { code: "opuo-parc", cname: "Parc" },
    { code: "oprc-sport", cname: "Complexe sportif" }, // Ajustez si 'Complexe sportif' sous 'Semi-privé Couvert' a un cname différent
    { code: "opro-sport", cname: "Complexe sportif" }, // Ajustez si 'Complexe sportif' sous 'Semi-privé Non Couvert' a un cname différent
  ];

  const dispatch = useDispatch();

  const updateView = (value) => {
    setView(value);
  };
  function prepareData() {
    let p = [];
    let un = [];
    for (let i = 0; i < days.length; i++) {
      p.push({
        id: i,
        day: days[i],
        start:
          new Date(terminalData.week_schedule[days[i]].debut).getHours() +
          ":" +
          new Date(terminalData.week_schedule[days[i]].debut).getMinutes(),
        end:
          new Date(terminalData.week_schedule[days[i]].fin).getHours() +
          ":" +
          new Date(terminalData.week_schedule[days[i]].fin).getMinutes(),
        duration:
          new Date(terminalData.week_schedule[days[i]].fin) -
          new Date(terminalData.week_schedule[days[i]].debut),
      });
    }
    setPlanning(p);
    terminalData?.unavailable_dates.forEach((value, index) => {
      let u = {
        start_date: value.start_date,
        end_date: value.end_date,
        num: index,
      };

      un.push(u);
    });
    setUnavailableDates(un);
  }
  function navigateToKiosk(id) {
    navigate(`/kiosk/${id}`);
  }
  function activateKiosk() {
    setTerminalData({ ...terminalData, is_active: !terminalData.is_active });
  }
  const searchPlace = async (query) => {
    const p = [
      "Centre commercial",
      "Marcahé de Rungis",
      "FitnessPark Boissy",
      "Université Paris Créteil",
    ];
    setPlaces(p);
  };
  const debouncedSearchPlace = useCallback(_.debounce(searchPlace, 500), []);
  function changeCalendarView(date) {
    setDates(date);
    setViewDate(date);
  }
  function getSelectedDate(date) {
    setViewDate(date);
    setDates(date);
    if (date) {
      if (date[1]) {
        if (selectedUnavailableDate) {
          unavailableDates[selectedUnavailableDate.num].start_date = date[0];
          unavailableDates[selectedUnavailableDate.num].end_date = date[1];
          setEditing(true);
        } else {
          unavailableDates.push({
            start_date: date[0],
            end_date: date[1],
            num: unavailableDates.length,
          });
          setEditing(true);
        }
      }
    } else {
      setDates(date);
    }
  }
  function deleteDate() {
    setEditing(true);
    unavailableDates.splice(selectedUnavailableDate.num, 1);
    setDates(null);
    setSelectedUnavailableDate(null);
    // saveTerminal()
  }
  function getUnavailable(date) {
    if (date) {
      setSelectedUnavailableDate(date);
      setViewDate([new Date(date.start_date), new Date(date.end_date)]);
      setDates([new Date(date.start_date), new Date(date.end_date)]);
    } else {
      setDates(new Date());
    }
  }
  async function saveTerminal() {
    let ud;
    for (let i = 0; i < unavailableDates.length; i++) {
      delete unavailableDates[i]["num"];
    }
    let body = {
      unavailable_dates: unavailableDates,
    };

    try {
      const resp = await api.patch("/terminal/" + terminalData.id, body);
      if (resp.status === 200) {
        toast.current.show({
          severity: "success",
          summary: "Success Message",
          detail: "Modifications enregistrées",
        });
        dispatch(updateKiosk(resp.data.terminal));
        setVisible(false);
        initVars();
      }
    } catch (error) {
      console.error(error);
      if (error.status == 422) {
        toast.current.show({
          severity: "error",
          summary: "Informations error",
          detail: "Echec de la modification",
        });
      } else {
        toast.current.show({
          severity: "error",
          summary: "Error Message",
          detail: "Echec de la modification",
        });
      }
    }
  }
  function initVars() {
    setVisible(false);
    setSelectedUnavailableDate(null);
    setDates(new Date());
    setEditing(false);
  }
  function openModal() {
    prepareData();
    setVisible(true);
  }
  function findCNameByCode(code) {
    const mapping = codeToCNameMap.find((item) => item.code === code);
    return mapping ? mapping.cname : "Code non trouvé";
  }
  const handleNameChange = (event) => {
    setName(event.target.value);
  };
  const handleDescriptionChange = (event) => {
    setDescription(event.target.value);
  };
  const hasNameChanges = () => {
    return name !== terminalData?.name;
  };
  const hasDescriptionChanges = () => {
    return description !== terminalData?.description;
  };
  const hasTypologyChanges = () => {
    return selectedTypology !== findCNameByCode(terminalData?.place_type);
  };
  const toggleEditTypology = () => {
    console.log("toto");
    setIsEditingTypology(!isEditingTypology);
  };
  const toggleEditName = () => {
    setIsEditingName(!isEditingName);
  };
  const toggleEditDescription = () => {
    setIsEditingDescription(!isEditingDescription);
  };
  const saveTypology = async () => {
    // Exemple de mise à jour de l'état local (ajustez selon vos besoins)
    const success = await callTerminalUpdate();
    if (success) {
      setTerminalData((prevData) => ({
        ...prevData,
        place_type: selectedTypology.code,
      }));
      toast.current.show({
        severity: "success",
        summary: "Succès",
        detail: "La typology a été mise à jour avec succès.",
        life: 3000,
      });
      setIsEditingTypology(false); // Quitter le mode d'édition après la sauvegarde
    }
  };
  const handleTypologyChange = (e) => {
    setSelectedTypology(e.value);
  };
  const saveDescription = async () => {
    // Logique pour enregistrer la description...
    const success = await callTerminalUpdate();
    if (success) {
      setTerminalData((prevData) => ({
        ...prevData,
        description: description, // Mise à jour avec la nouvelle valeur
      }));
      // Afficher un toast de succès
      toast.current.show({
        severity: "success",
        summary: "Succès",
        detail: "La description a été mise à jour avec succès.",
        life: 3000,
      });
      setIsEditingDescription(false); // Quitter le mode d'édition après la sauvegarde
    } else {
      // Afficher un toast d'erreur si nécessaire
      toast.current.show({
        severity: "error",
        summary: "Erreur",
        detail: "La mise à jour de la description a échoué.",
        life: 3000,
      });
    }
  };
  const saveName = async () => {
    // Logique pour enregistrer le nom...
    const success = await callTerminalUpdate();
    if (success) {
      setTerminalData((prevData) => ({
        ...prevData,
        name: name, // Mise à jour avec la nouvelle valeur
      }));
      setIsEditingName(false); // Quitter le mode d'édition après la sauvegarde
      toast.current.show({
        severity: "success",
        summary: "Succès",
        detail: "Le nom a été mise à jour avec succès.",
        life: 3000,
      });
    }
  };
  const updateTerminal = async (field, value) => {
    const success = await callTerminalUpdate(field, value);
    if (success) {
      setTerminalData((prevData) => ({
        ...prevData,
        [field]: value,
      }));
      toast.current.show({
        severity: "success",
        summary: "Succès",
        detail: `${field} a été mise à jour avec succès.`,
        life: 3000,
      });
    } else {
      toast.current.show({
        severity: "error",
        summary: "Erreur",
        detail: `La mise à jour de ${field} a échoué.`,
        life: 3000,
      });
    }
  };
  const callTerminalUpdate = async () => {
    // console.log("callTerminalUpdate called");
    const headers = {
      accept: "application/json",
      "Content-Type": "application/json",
    };

    const fieldsToUpdate = {};
    if (hasNameChanges()) {
      fieldsToUpdate.name = sanitizeInput(name);
    }
    if (hasDescriptionChanges()) {
      fieldsToUpdate.description = sanitizeInput(description);
    }
    if (hasTypologyChanges()) {
      // Utilisez ici la nouvelle fonction
      // console.log("selectedTypology", selectedTypology);
      fieldsToUpdate.place_type = selectedTypology.code;
    }
    // Add more fields to update as necessary, similar to the checks above

    if (Object.keys(fieldsToUpdate).length === 0) {
      //   console.log("No changes to update");
      return false;
    }
    // console.log("fieldsToUpdate", fieldsToUpdate);
    try {
      const resp = await api.patch(
        `/terminal/${terminalData?.id}`,
        fieldsToUpdate,
        { headers }
      );
      if (resp.status === 200) {
        dispatch(updateKiosk(resp.data.terminal));
        setShowError(true);
      }
      console.log("resp", resp);
      if (resp.status !== 200) {
        return false;
      }
      return true;
    } catch (error) {
      // console.error("error", error);
      setShowWarn(true);
      return false;
    }
  };
  const unAvailableTemplate = (option) => {
    return (
      <div className="">
        <div className="list-none font-bold text-xs my-2 flex w-max justify-content-center text-center">
          <span className="border-1 border-round-2xl px-1 hours hours-txt bg-white mx-1 ">
            {convertDate(option.start_date)}
          </span>
          <hr
            className="inline-block mr-1"
            style={{ width: "15px", height: "1px" }}
          />
          <span className="border-1 border-round-2xl  hours-txt px-1 bg-white hours">
            {convertDate(option.end_date)}
          </span>
        </div>
      </div>
    );
  };

  return (
    <div className="ctnr">
      <div className="flex">
        <div className="text-left flex-initial">
          <div className="mt-0 mb-5 flex align-items-center">
            {" "}
            <i
              className="pi pi-arrow-left text-3xl mr-3 text-black-alpha-80 arrow-hover"
              onClick={() => navigate("/kiosks")}
            ></i>
            {isEditingName ? (
              <div
                style={{
                  flex: 1,
                  display: "flex",
                  alignItems: "center",
                }}
              >
                <input
                  type="text"
                  className="p-inputtext p-component"
                  value={name}
                  onChange={handleNameChange}
                  style={{ flexGrow: 1 }}
                />
                {hasNameChanges() && (
                  <button
                    className="p-button p-component"
                    onClick={saveName}
                    style={{ marginLeft: "10px" }}
                  >
                    Save
                  </button>
                )}
                {/* Ajout d'un bouton ou icône pour annuler l'édition */}
                <i
                  className="pi pi-times edit-icon"
                  style={{
                    marginLeft: "10px",
                    cursor: "pointer",
                  }}
                  onClick={toggleEditName}
                ></i>
              </div>
            ) : (
              <div
                style={{
                  flex: 1,
                  display: "flex",
                  alignItems: "center",
                }}
              >
                <span
                  className="text-3xl font-bold"
                  style={{ flexGrow: 1 }}
                  onDoubleClick={toggleEditName}
                >
                  {terminalData?.name}
                </span>
                {/* Icône de crayon visible lorsque pas en mode édition */}
                <i
                  className="pi pi-pencil edit-icon"
                  style={{
                    cursor: "pointer",
                    marginLeft: "10px",
                  }}
                  onClick={toggleEditName}
                ></i>
              </div>
            )}
          </div>
        </div>

        <div
          className="text-right flex  justify-content-end flex-auto mb-5"
          id="newKioskDiv"
        >
          <div className="mt-2 mr-3">
            <span className="">
              <i
                className={
                  terminalData?.is_active
                    ? "text-green-500 text-xs pi pi-circle-on m-2"
                    : "txt-red-custom text-xs pi pi-circle-on m-2"
                }
              ></i>
              {terminalData?.is_active ? "online" : "offline"}
            </span>
          </div>
          <div className="card justify-content-center mt-2 mr-2 ">
            <InputSwitch
              className="m-"
              checked={terminalData?.is_active}
              // onChange={(e) => activateKiosk()}
              disabled
            />
          </div>
        </div>
      </div>
      <div className="grid">
        <div className="col-9 md:col-9 sm:col-12">
          <div className="grid bloc info-stats">
            <div className="col ">
              <div className="flex">
                <ul className="list-none p-0 text-right mx-1">
                  <li className="bloc-title ">ID Machine</li>
                  <li className="bloc-title">Adresse IP</li>
                  <li className="bloc-title">Crée</li>
                  <li className="bloc-title"> Localisation</li>
                  <li className="bloc-title"> Dernière Intervention</li>
                  <li className="bloc-title"> Propriétaire</li>
                </ul>
                <ul className="text-left list-none p-0 ">
                  <li className="bloc-value camp-info">{terminalData?.id}</li>
                  <li className="bloc-value">105.103.96.202</li>
                  <li className="bloc-value camp-info">
                    {convertDate(terminalData?.start_date)}
                  </li>
                  <li className="bloc-value camp-info">
                    {terminalData?.localisation}
                  </li>
                  <li className="bloc-value camp-info">12/02/2024</li>
                  <li className="bloc-value camp-info">
                    {terminalData?.distributor_id}
                  </li>
                </ul>
              </div>
            </div>
            <div className="col flex stat_blocs justify-content-center ">
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
        <div className="col-3 md:col-3 sm:col-12">
          <div className="col bloc mt-0">
            <div className="flex justify-content-center sm:justify-content-start flex-column flex-wrap align-items-center align-content-center">
              <h5 className="mt-2">Others devices</h5>
              <ListBox
                onChange={(e) => navigateToKiosk(e.value.id)}
                options={terminals}
                optionLabel="name"
                className="w-full"
                listStyle={{
                  maxHeight: "200px",
                  fontSize: "12px",
                }}
              />
            </div>
          </div>
        </div>
      </div>
      <div className="grid ">
        <div className="col-6 sm:col-12 md:col-6 pl-0 pt-0 ">
          <div className="bloc p-3">
            <div className="">
              <span className="bloc-title">
                Description Détaillée de l'emplacement
              </span>
              {/* Icône conditionnelle basée sur le mode d'édition */}
              {isEditingDescription ? (
                <i
                  className="pi pi-times edit-icon"
                  style={{
                    float: "right",
                    cursor: "pointer",
                  }}
                  onClick={toggleEditDescription}
                ></i>
              ) : (
                <i
                  className="pi pi-pencil edit-icon"
                  style={{
                    float: "right",
                    cursor: "pointer",
                  }}
                  onClick={toggleEditDescription}
                ></i>
              )}
            </div>
            {isEditingDescription ? (
              <div>
                <textarea
                  className="p-inputtext p-component p-inputtextarea"
                  value={description}
                  onChange={handleDescriptionChange}
                  rows="5"
                  style={{ width: "100%" }}
                ></textarea>
                {hasDescriptionChanges() && (
                  <button
                    className="p-button p-component"
                    onClick={saveDescription}
                    style={{ marginTop: "10px" }}
                  >
                    Save
                  </button>
                )}
              </div>
            ) : (
              <p className="text-600 p-2 bloc-value">
                {terminalData?.description}
              </p>
            )}
          </div>
        </div>
        <div className="col-6 sm:col-12 md:col-6 h-auto items-center justify-center bloc">
          <div className=" mx-2">
            <div className="">
              <span className="m-2 bloc-title">Type d'emplacement</span>
              {isEditingTypology ? (
                <i
                  className="pi pi-times edit-icon"
                  style={{
                    float: "right",
                    cursor: "pointer",
                  }}
                  onClick={toggleEditTypology}
                ></i>
              ) : (
                <i
                  className="pi pi-pencil edit-icon"
                  style={{
                    float: "right",
                    cursor: "pointer",
                  }}
                  onClick={toggleEditTypology}
                ></i>
              )}
            </div>
          </div>

          <div className="m-auto text-center p-2 my-7 ">
            <CascadeSelect
              inputId="cs-kiosk-typo"
              value={selectedTypology}
              onChange={handleTypologyChange}
              options={typoOptions}
              optionLabel="cname"
              optionGroupLabel="name"
              optionGroupChildren={["mainCat", "categories", "categories"]}
              breakpoint="767px"
              style={{ minWidth: "100%" }}
              className="border-1 border-round-3xl border-purple-500 font-semibold"
              disabled={!isEditingTypology}
            />
            {isEditingTypology &&
              hasTypologyChanges() && ( // Afficher le bouton de sauvegarde uniquement en mode d'édition
                <button
                  className="p-button p-component"
                  onClick={saveTypology}
                  style={{ marginTop: "10px" }}
                >
                  Save
                </button>
              )}
          </div>
        </div>
      </div>
      <div className="grid">
        <div className="col-6 md:col-6 sm:col-12 pl-0 ">
          <div className="bloc p-3">
            <div className="">
              <i className="pi pi-pencil" style={{ float: "right" }}></i>
            </div>
            <div className="w-100 overflow-hidden overflow-x-scroll">
              <ul className="list-none flex text-center p-0 w-max">
                {planning.map((item, index) => (
                  <li className="text-center mr-2" key={index}>
                    <span className="bloc-title">{item.day}</span>
                    <div
                      className={
                        item.duration > 0 ? "text-green-500" : "text-gray-500"
                      }
                    >
                      <i className=" pi pi-circle-on "></i>
                    </div>
                    {item.duration > 0 ? (
                      <span
                        className="border-1 w-max border-round-2xl px-1 bg-white hours hours-txt"
                        style={{
                          fontSize: "10px",
                          width: "auto",
                          borderColor: "#5C69FE",
                        }}
                      >
                        {item.start} - {item.end}
                      </span>
                    ) : (
                      <span
                        className="border-1 border-round-2xl px-5 bg-gray-500  hours-txt"
                        style={{ fontSize: "10px", borderColor: "#5C69FE" }}
                      ></span>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
        <div className="col-6 md:col-6 sm:col-12">
          <div className="bloc p-3 ">
            <div className="">
              <span className="bloc-title">Date d'indisponibilité</span>
              <i
                className="pi pi-pencil"
                style={{ float: "right" }}
                onClick={() => openModal()}
              ></i>
            </div>
            {terminalData?.unavailable_dates.map((date, index) => (
              <div
                className="list-none font-bold text-xs my-2 text-center"
                key={index}
              >
                <span className="border-1 border-round-2xl px-1 hours hours-txt bg-white mx-1 ">
                  {convertDate(date.start_date)}
                </span>
                <hr
                  className="inline-block m-1 border-top-1"
                  style={{ width: "15px" }}
                />
                <span className="border-1 border-round-2xl  hours-txt px-1 bg-white hours">
                  {convertDate(date.end_date)}
                </span>
              </div>
            ))}
            <div className="card flex justify-content-center ">
              <Dialog
                header="Indisponibilités"
                visible={visible}
                style={{ width: "75vw" }}
                onHide={() => initVars()}
              >
                <div className="grid">
                  <div className="col-4">
                    <div className="card">
                      <div className="card ">
                        <div>
                          <ListBox
                            value={selectedUnavailableDate}
                            onChange={(e) => getUnavailable(e.value)}
                            options={unavailableDates}
                            itemTemplate={unAvailableTemplate}
                            className="w-full md:w-17rem"
                            listStyle=""
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="col-2">
                    <div className="m-auto text-center flex flex-column">
                      {selectedUnavailableDate && (
                        <Button
                          onClick={() => deleteDate()}
                          icon="pi pi-trash"
                          label="Supprimer"
                          severity="danger"
                          text
                        />
                      )}
                      {editing && (
                        <Button
                          onClick={() => saveTerminal()}
                          icon="pi pi-check"
                          label="Valider"
                          severity="success"
                          text
                        />
                      )}
                      {(editing || selectedUnavailableDate) && (
                        <Button
                          onClick={() => initVars()}
                          icon="pi pi-refresh"
                          label="Annuler"
                          severity="primary"
                          text
                        />
                      )}
                    </div>
                  </div>
                  <div className="col-6">
                    <Calendar
                      ref={calendarRef}
                      value={SelectedDates}
                      onChange={(e) => getSelectedDate(e.value)}
                      selectionMode="range"
                      style={{ width: "100%" }}
                      minDate={new Date()}
                      onViewDateChange={(e) => changeCalendarView(e.value)}
                      locale="fr"
                      showTime
                      inline
                    />
                  </div>
                </div>
              </Dialog>
            </div>
          </div>
        </div>
      </div>
      <Toast ref={toast}></Toast>
    </div>
  );
}
