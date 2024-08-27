import React, { useState, useCallback, useRef, useEffect } from "react";
import axios from "axios";
import { Button } from "primereact/button";
import { Dialog } from "primereact/dialog";
import { InputText } from "primereact/inputtext";
import { CascadeSelect } from "primereact/cascadeselect";
import { InputTextarea } from "primereact/inputtextarea";
import { ProgressBar } from "primereact/progressbar";
import { Toast } from "primereact/toast";
import { Calendar } from "primereact/calendar";
import { Checkbox } from "primereact/checkbox";
import { AutoComplete } from "primereact/autocomplete";
import { useDispatch } from "react-redux";
import { addKiosk } from "../../services/store/kiosksSlice";
import "primeicons/primeicons.css";
import "primereact/resources/primereact.css";
import "primeflex/primeflex.scss";
import { InputSwitch } from "primereact/inputswitch";
import { Steps } from "primereact/steps";
import _ from "lodash";
import SimpleMap from "../SimpleMap";

import { api } from "../../services/config";
import { convertDateTimeToDate, typoOptions } from "../../services/utils";
import { PopUp } from "../../styles/PopUp.scss";

export default function NewKiosk({ showCreateModal, setShowCreateModal }) {
  const [showModal, setShowModal] = useState(1);
  const toast = useRef(null);
  const dispatch = useDispatch();

  const [progress, setProgress] = useState(0);
  const [name, setName] = useState("");
  const [selectedTypology, setSelectedTypology] = useState(null);
  const [details, setDetails] = useState("");
  const [address, setAddress] = useState("");
  const [showMarker, setShowMarker] = useState(false);
  const [lat, setLat] = useState(48.85837); // Valeur initiale pour la latitude
  const [lng, setLng] = useState(2.294481);
  const [startFrom, setStartFrom] = useState(undefined);
  const [unavailableDates, setUnavailableDates] = useState([]);
  const [weekSchedule, setWeekSchedule] = useState({
    lundi: {
      debut: new Date(new Date().setHours(8, 0)),
      fin: new Date(new Date().setHours(20, 0)),
    },
    mardi: {
      debut: new Date(new Date().setHours(8, 0)),
      fin: new Date(new Date().setHours(20, 0)),
    },
    mercredi: {
      debut: new Date(new Date().setHours(8, 0)),
      fin: new Date(new Date().setHours(20, 0)),
    },
    jeudi: {
      debut: new Date(new Date().setHours(8, 0)),
      fin: new Date(new Date().setHours(20, 0)),
    },
    vendredi: {
      debut: new Date(new Date().setHours(8, 0)),
      fin: new Date(new Date().setHours(20, 0)),
    },
    samedi: {
      debut: new Date(new Date().setHours(8, 0)),
      fin: new Date(new Date().setHours(20, 0)),
    },
    dimanche: {
      debut: new Date(new Date().setHours(8, 0)),
      fin: new Date(new Date().setHours(20, 0)),
    },
  });
  const [filteredAddresses, setFilteredAddresses] = useState([]);

  const searchAddress = async (query) => {
    if (typeof query !== "string" || !query.trim()) return;

    try {
      const { data } = await axios.get(
        `https://nominatim.openstreetmap.org/search?addressdetails=1&q=${query}&format=json&countrycodes=fr`
      );
      setFilteredAddresses(data);
    } catch (error) {
      console.error("Error while fetching addresses:", error);

      toast.current.show({
        severity: "error",
        summary: "Error Message",
        detail: "Error while fetching addresses",
      });
    }
  };

  const debouncedSearchAddress = useCallback(
    _.debounce(searchAddress, 500),
    []
  );

  async function PostNewKiosk() {
    let body = {
      place_type: selectedTypology.code,
      name: name,
      description: details,
      localisation: address.display_name,
      lat: address.lat,
      long: address.lon,
      start_date: startFrom,
      week_schedule: weekSchedule,
      unavailable_dates: unavailableDates.map(([start_date, end_date]) => ({
        start_date,
        end_date,
      })),
      // last_update: convertDateTimeToDate(new Date()),
    };

    try {
      const resp = await api.post("/terminal", body);
      if (resp.status === 200) {
        toast.current.show({
          severity: "success",
          summary: "Success Message",
          detail: "Kiosk added",
        });

        setShowCreateModal(false);

        dispatch(addKiosk(resp.data));
      }
    } catch (error) {
      console.error(error);
      if (error.status == 422) {
        toast.current.show({
          severity: "error",
          summary: "Informations error",
          detail: "Kiosk already exists",
        });
      } else {
        toast.current.show({
          severity: "error",
          summary: "Error Message",
          detail: "Kiosk not added",
        });
      }
    }
  }

  function checkInputsModal(index) {
    let nextModal = true;

    switch (index) {
      case 1:
        if (name == "" || !name) {
          document.getElementById("kiosk-name").classList.add("p-invalid");
          nextModal = false;
        } else {
          document
            .getElementById("kiosk-name")
            .classList.contains("p-invalid") ? (
            document.getElementById("kiosk-name").classList.remove("p-invalid")
          ) : (
            <></>
          );
        }

        if (!selectedTypology || selectedTypology == "") {
          document.getElementById("cs-kiosk-typo").classList.add("p-invalid");
          nextModal = false;
        } else {
          document
            .getElementById("cs-kiosk-typo")
            .classList.contains("p-invalid") ? (
            document
              .getElementById("cs-kiosk-typo")
              .classList.remove("p-invalid")
          ) : (
            <></>
          );
        }

        if (!details || details == "") {
          document.getElementById("kiosk-details").classList.add("p-invalid");
          nextModal = false;
        } else {
          document
            .getElementById("kiosk-details")
            .classList.contains("p-invalid") ? (
            document
              .getElementById("kiosk-details")
              .classList.remove("p-invalid")
          ) : (
            <></>
          );
        }
        if (!address || address == "") {
          document
            .getElementById("display_address_input")
            .classList.add("p-invalid");
          nextModal = false;
        } else {
          document
            .getElementById("display_address_input")
            .classList.contains("p-invalid") ? (
            document
              .getElementById("display_address_input")
              .classList.remove("p-invalid")
          ) : (
            <></>
          );
        }
        break;

      case 2:
        if (!startFrom || startFrom == "") {
          document
            .getElementById("kiosk-start-date")
            .classList.add("p-invalid");
          nextModal = false;
        } else {
          document
            .getElementById("kiosk-start-date")
            .classList.contains("p-invalid") ? (
            document
              .getElementById("kiosk-start-date")
              .classList.remove("p-invalid")
          ) : (
            <></>
          );
        }

        Object.keys(weekSchedule).map((day) => {
          if (!weekSchedule[day].debut || weekSchedule[day].debut == "") {
            document
              .getElementById(`${day}-kiosk-name-1`)
              .classList.add("p-invalid");
            nextModal = false;
          } else {
            document
              .getElementById(`${day}-kiosk-name-1`)
              .classList.contains("p-invalid") ? (
              document
                .getElementById(`${day}-kiosk-name-1`)
                .classList.remove("p-invalid")
            ) : (
              <></>
            );
          }
          if (!weekSchedule[day].fin || weekSchedule[day].fin == "") {
            document
              .getElementById(`${day}-kiosk-name-2`)
              .classList.add("p-invalid");
            nextModal = false;
          } else {
            document
              .getElementById(`${day}-kiosk-name-2`)
              .classList.contains("p-invalid") ? (
              document
                .getElementById(`${day}-kiosk-name-2`)
                .classList.remove("p-invalid")
            ) : (
              <></>
            );
          }
        });

        if (unavailableDates.length > 0) {
          unavailableDates.map((dateRange, index) => {
            if (!dateRange[0] || dateRange[0] == "") {
              document
                .getElementById(`calendar-unav-input-${index}`)
                .classList.add("p-invalid");
              nextModal = false;
            } else if (!dateRange[1] || dateRange[1] == "") {
              document
                .getElementById(`calendar-unav-input-${index}`)
                .classList.add("p-invalid");
              nextModal = false;
            } else {
              document
                .getElementById(`calendar-unav-input-${index}`)
                .classList.contains("p-invalid") ? (
                document
                  .getElementById(`calendar-unav-input-${index}`)
                  .classList.remove("p-invalid")
              ) : (
                <></>
              );
            }
          });
        }

        break;

      default:
        break;
    }

    return nextModal;
  }

  function incrementModal() {
    let nb = showModal;
    if (checkInputsModal(nb)) {
      setShowModal(nb + 1);
      setProgress(progress + 50);
    }
  }

  function decrementModal() {
    let nb = showModal;
    setShowModal(nb - 1);
    setProgress(progress - 50);
  }

  // Méthode pour mettre à jour l'adresse et les coordonnées
  const handleAddressChange = (e) => {
    setAddress(e.value); // Met à jour l'adresse
    if (e.value.lat && e.value.lon) {
      setLat(parseFloat(e.value.lat)); // Met à jour la latitude
      setLng(parseFloat(e.value.lon)); // Met à jour la longitude
      setShowMarker(true);
    }
  };

  const footerContent = (
    <>
      <div className="points-footer">
        <div className="p-d-flex p-jc-center">
          <div className={`point ${showModal === 1 ? "active" : ""}`}></div>
          <div className={`point ${showModal === 2 ? "active" : ""}`}></div>
          <div className={`point ${showModal === 3 ? "active" : ""}`}></div>
        </div>
      </div>
      <div className="button-footer">
        {showModal > 1 ? (
          <Button
            label="Retour"
            onClick={() => decrementModal()}
            className="btn-secondary"
            // severity="danger"
            outlined
          />
        ) : (
          <></>
        )}
        {showModal < 3 ? (
          <Button
            label="Suivant"
            onClick={() => incrementModal()}
            autoFocus
            className="btn-primary"
          />
        ) : (
          <></>
        )}
        {showModal == 3 ? (
          <Button
            label="Souvegarder"
            icon="pi pi-check"
            onClick={() => {
              PostNewKiosk();
              // setShowCreateModal(false);
            }}
            autoFocus
            className="btn-primary"
          />
        ) : (
          <></>
        )}
      </div>
    </>
  );

  useEffect(() => {
    const addressString =
      typeof address === "string" ? address : address?.display_name || "";
    if (addressString.trim()) {
      debouncedSearchAddress(addressString);
    } else {
      setFilteredAddresses([]);
    }
  }, [address, debouncedSearchAddress]);

  const reInit = () => {
    setShowCreateModal(false);
    setShowModal(1);
    setProgress(0);
    setName("");
    setSelectedTypology(null);
    setDetails("");
    setAddress("");
    setStartFrom(undefined);
    setUnavailableDates([]);
    setWeekSchedule({
      lundi: { debut: undefined, fin: undefined },
      mardi: { debut: undefined, fin: undefined },
      mercredi: { debut: undefined, fin: undefined },
      jeudi: { debut: undefined, fin: undefined },
      vendredi: { debut: undefined, fin: undefined },
      samedi: { debut: undefined, fin: undefined },
      dimanche: { debut: undefined, fin: undefined },
    });
    setShowMarker(false);
  };

  return (
    <div className="card flex justify-content-center">
      <Dialog
        header="Nouvelle borne"
        visible={showCreateModal}
        onHide={reInit}
        footer={footerContent}
        style={{ width: "90vw" }}
        breakpoints={{ "960px": "75vw", "641px": "100vw" }}
        maximizable
      >
        {showModal === 1 && (
          <div className="card justify-content-center mt-5 pop-container-centered">
            <div className="flex flex-wrap justify-content-around">
              <div className="flex flex-column">
                <div className="mb-5">
                  <span className="span-input-contain font-bold">
                    <label htmlFor="kiosk-name" className="text-color-label">
                      Nom de la Borne *
                    </label>
                    <InputText
                      id="kiosk-name"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      className="border-1  border-primary-color font-semibold"
                    />
                  </span>
                </div>
                <div className="mb-5">
                  <span className="span-input-contain font-bold">
                    <label htmlFor="cs-kiosk-typo" className="text-color-label">
                      Location Typology *
                    </label>
                    <CascadeSelect
                      inputId="cs-kiosk-typo"
                      // id="cs-kiosk-typo"
                      value={selectedTypology}
                      onChange={(e) => setSelectedTypology(e.value)}
                      options={typoOptions}
                      optionLabel="cname"
                      optionGroupLabel="name"
                      optionGroupChildren={[
                        "mainCat",
                        "categories",
                        "categories",
                      ]}
                      //   className="w-full md:w-14rem"
                      breakpoint="767px"
                      style={{ minWidth: "14rem" }}
                      className="border-1  border-primary-color font-semibold"
                    />
                    {/* <label>Location Typology *</label> */}
                  </span>
                </div>
                <div className="mb-5">
                  <span className="span-input-contain font-bold">
                    <label htmlFor="kiosk-details" className="text-color-label">
                      {" "}
                      Description Détaillée *
                    </label>
                    <InputTextarea
                      className="inputFW border-1  border-primary-color font-semibold"
                      id="kiosk-details"
                      value={details}
                      onChange={(e) => setDetails(e.target.value)}
                      rows={2}
                      autoResize
                    />
                  </span>
                </div>
              </div>
              <div className="flex flex-column">
                <div className="mb-5">
                  <span className="span-input-contain font-bold">
                    <label
                      htmlFor="display_address_input"
                      className="text-color-label"
                    >
                      {" "}
                      Adresse *
                    </label>
                    <AutoComplete
                      className="inputFW p-fluid"
                      inputClassName="border-1  border-primary-color font-semibold"
                      id="display_address"
                      inputId="display_address_input"
                      value={address.display_name || address}
                      suggestions={filteredAddresses}
                      completeMethod={(e) => setAddress(e.query)}
                      // field="kiosk-adresse"
                      field="display_name"
                      onChange={handleAddressChange}
                    />
                    <div className="map-born">
                      <SimpleMap lat={lat} lng={lng} showMarker={showMarker}/>
                    </div>
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}
        {showModal === 2 && (
          <div className="card justify-content-center mt-5">
            {/* Date DEBUT */}
            <div className="flex flex-wrap justify-content-around">
              <div className="flex flex-column md:w-6 left-content-end">
                <div className="mb-5 flex justify-content-center">
                  <span className="span-input-contain justify-content-start date-start font-bold border-date-primary">
                    <label
                      htmlFor="kiosk-name"
                      className="text-color-label"
                      style={{ textAlign: "center" }}
                    >
                      Date de début
                    </label>
                    <Calendar
                      inputClassName="border-round-left-3xl border-right-none border-primary-color font-semibold"
                      value={startFrom}
                      onChange={(e) => {
                        setStartFrom(e.value);
                      }}
                      id="kiosk-start-date"
                      minDate={new Date()}
                      locale="fr"
                      showIcon
                      readOnlyInput
                      showTime
                      showButtonBar
                      dateFormat="dd/mm/yy"
                    />
                  </span>
                </div>

                <section className="grid horaires-section">
                  <div className="col-12 text-center text-color-label font-bold">
                    Horaires hebdomadaires
                  </div>
                  {Object.keys(weekSchedule).map((day) => (
                    <div
                      className="col-12 mb-1 flex flex-column days-week"
                      key={`col-${day}`}
                    >
                      <div
                        className="flex flex-row day"
                        key={`col-${day}-div`}
                        style={{
                          flexWrap: "nowrap",
                          justifyContent: "center",
                          alignItems: "center",
                        }}
                      >
                        <span
                          className=" flex flex-nowrap align-items-center"
                          key={`col-${day}-div-span-3`}
                          style={{
                            textAlign: "center",
                            padding: "0 15px 0 0px",
                          }}
                        >
                          <InputSwitch
                            onChange={(e) => {
                              if (!e.value) {
                                // If the switch is turned on (closed)
                                setWeekSchedule((weekSchedule) => ({
                                  ...weekSchedule,
                                  [day]: {
                                    ...weekSchedule[day],
                                    debut: new Date(
                                      new Date().setHours(0, 0, 0, 0)
                                    ),
                                    fin: new Date(
                                      new Date().setHours(0, 0, 0, 0)
                                    ),
                                  },
                                }));
                              } else {
                                // If the switch is turned off (open)
                                setWeekSchedule((weekSchedule) => ({
                                  ...weekSchedule,
                                  [day]: {
                                    ...weekSchedule[day],
                                    debut: new Date(
                                      new Date().setHours(0, 0, 0, 0)
                                    ), // Adjust as needed
                                    fin: new Date(
                                      new Date().setHours(0, 1, 0, 0)
                                    ), // Adjust as needed
                                  },
                                }));
                              }
                            }}
                            checked={
                              !(
                                weekSchedule[day].debut &&
                                weekSchedule[day].debut.getHours() === 0 &&
                                weekSchedule[day].debut.getMinutes() === 0 &&
                                weekSchedule[day].fin &&
                                weekSchedule[day].fin.getHours() === 0 &&
                                weekSchedule[day].fin.getMinutes() === 0
                              )
                            }
                          />
                          <span
                            className="span-input-contain text-color-label"
                            style={{
                              margin: "0 0 0 15px",
                              width: "84px",
                              textAlign: "left",
                              textTransform: "Capitalize",
                            }}
                            key={`col-${day}-span`}
                          >
                            {day}
                          </span>
                        </span>
                        <span
                          className="span-input-contain"
                          key={`col-${day}-div-span-1`}
                        >
                          <Calendar
                            // value={weekSchedule[day].debut}
                            // value={weekSchedule[day].debut || new Date(new Date().setHours(8, 0))}
                            value={
                              weekSchedule[day].debut !== undefined &&
                              weekSchedule[day].debut !== null
                                ? weekSchedule[day].debut
                                : new Date(new Date().setHours(8, 0))
                            }
                            inputClassName="border-1  border-primary-color max-w-5rem"
                            onChange={(e) => {
                              setWeekSchedule((weekSchedule) => ({
                                ...weekSchedule,
                                [day]: { ...weekSchedule[day], debut: e.value },
                              }));
                            }}
                            key={`col-${day}-div-calendar-1`}
                            id={`${day}-kiosk-name-1`}
                            disabled={
                              weekSchedule[day].debut !== undefined &&
                              weekSchedule[day].debut !== null &&
                              weekSchedule[day].debut.getHours() === 0 &&
                              weekSchedule[day].debut.getMinutes() === 0 &&
                              weekSchedule[day].fin !== undefined &&
                              weekSchedule[day].fin !== null &&
                              weekSchedule[day].fin.getHours() === 0 &&
                              weekSchedule[day].fin.getMinutes() === 0
                            }
                            hourFormat="24"
                            readOnlyInput
                            timeOnly
                          />
                          {/*<label*/}
                          {/*  htmlFor={`${day}-kiosk-name-1`}*/}
                          {/*  id={`${day}-kiosk-name-label-1`}*/}
                          {/*>*/}
                          {/*  From*/}
                          {/*</label>*/}
                        </span>
                        <span
                          className="span-input-contain"
                          key={`col-${day}-div-span-2`}
                          style={{ margin: "0 0 0 15px" }}
                        >
                          <Calendar
                            // value={weekSchedule[day].fin}
                            value={
                              weekSchedule[day].fin ||
                              new Date(new Date().setHours(20, 0))
                            }
                            inputClassName="border-1  border-primary-color max-w-5rem"
                            onChange={(e) => {
                              setWeekSchedule((weekSchedule) => ({
                                ...weekSchedule,
                                [day]: { ...weekSchedule[day], fin: e.value },
                              }));
                            }}
                            key={`col-${day}-div-calendar-2`}
                            id={`${day}-kiosk-name-2`}
                            disabled={
                              weekSchedule[day].debut &&
                              weekSchedule[day].debut.getHours() === 0 &&
                              weekSchedule[day].debut.getMinutes() === 0 &&
                              weekSchedule[day].fin &&
                              weekSchedule[day].fin.getHours() === 0 &&
                              weekSchedule[day].fin.getMinutes() === 0
                            }
                            hourFormat="24"
                            readOnlyInput
                            timeOnly
                          />
                          {/*<label*/}
                          {/*  htmlFor={`${day}-kiosk-name-2`}*/}
                          {/*  id={`${day}-kiosk-name-label-2`}*/}
                          {/*>*/}
                          {/*  To*/}
                          {/*</label>*/}
                        </span>
                      </div>
                    </div>
                  ))}
                </section>
              </div>
              {/* INDISPO */}
              <div className="flex flex-column md:w-6">
                <section className="mb-5 ">
                  <div
                    className="mb-4 text-center text-color-label font-bold"
                    style={{ fontSize: "20px" }}
                  >
                    Dates d'indisponibilités
                  </div>
                  <div className="flex justify-content-center">
                    <Button
                      onClick={() =>
                        setUnavailableDates((unavailableDates) => [
                          ...unavailableDates,
                          [],
                        ])
                      }
                      className="btn-primary"
                    >
                      Nouvelle indisponibilité +
                    </Button>
                  </div>
                  <div className="mb-5 mt-5">
                    {unavailableDates.length > 0 &&
                      unavailableDates.map((dateRange, index) => (
                        <div
                          className="mb-5 mt-5 flex flex-column"
                          key={`unav-${index}-div-1`}
                        >
                          <div
                            className="flex flex-row justify-content-center"
                            key={`unav-${index}-div1-div1`}
                          >
                            <span
                              className="span-input-contain justify-content-start date-start font-bold border-date-primary"
                              key={`unav-${index}-div1-div1-span1`}
                            >
                              <Calendar
                                inputClassName="border-round-left-3xl border-right-none border-primary-color font-semibold"
                                className="inputFW"
                                value={dateRange}
                                onChange={(e) => {
                                  const updatedDates = [...unavailableDates];
                                  updatedDates[index] = e.value;
                                  setUnavailableDates(updatedDates);
                                }}
                                key={`calendar-unav-input-${index}`}
                                id={`calendar-unav-input-${index}`}
                                minDate={new Date()}
                                selectionMode="range"
                                locale="fr"
                                readOnlyInput
                                showButtonBar
                                showTime
                                showIcon
                                dateFormat="dd/mm/yy"
                              />
                              {/*<label*/}
                              {/*  htmlFor={`calendar-unav-input-${index}`}*/}
                              {/*  key={`calendar-unav-input-${index}-label`}*/}
                              {/*>*/}
                              {/*  Indisponibilité*/}
                              {/*</label>*/}
                            </span>
                            <span
                              key={`unav-${index}-div1-div1-span2`}
                              style={{ display: "flex" }}
                            >
                              <Button
                                style={{
                                  margin: "0 0 0 15px",
                                  justifyContent: "center",
                                }}
                                onClick={() => {
                                  const updatedDates = [...unavailableDates];
                                  updatedDates.splice(index, 1);
                                  setUnavailableDates(updatedDates);
                                }}
                                // severity="danger"
                                className="btn-secondary"
                                key={`calendar-unav-btn-${index}`}
                              >
                                Supprimer
                              </Button>
                            </span>
                          </div>
                        </div>
                      ))}
                  </div>
                </section>
              </div>
            </div>
          </div>
        )}
        {showModal === 3 && (
          <div className="card justify-content-center mt-5">
            <div className="flex flex-wrap justify-content-around text-color-label mobile-left">
              <div className="flex flex-column md:w-6 left-content-end">
                <div className="mb-3">
                  <span className="span-input-contain ">
                    <strong>Nom :</strong> {name}
                  </span>
                </div>
                <div className="mb-3">
                  <span className="span-input-contain">
                    <strong>Typologie :</strong> {selectedTypology?.cname}
                  </span>
                </div>
                <div className="mb-3">
                  <span className="span-input-contain">
                    <strong>Adresse :</strong> {address?.display_name}
                  </span>
                </div>
                <div className="mb-3">
                  <span className="span-input-contain">
                    <strong>Description :</strong> {details}
                  </span>
                </div>
                <div className="mb-3">
                  <span className="span-input-contain">
                    <strong>Indisponibilités :</strong>{" "}
                    {unavailableDates.map(
                      (dateRange) => {
                        console.log(dateRange);
                        return dateRange
                          .map((date) => date.toLocaleString())
                          .join(" --- ");
                      }
                      // dateRange.map((date) => date).join(" --- ")
                      // error with date.toLocaleString()
                    )}
                  </span>
                </div>
              </div>
              <div className="flex flex-column md:w-6">
                <div className="mb-3">
                  <span
                    className="span-input-contain flex flex-column align-items-left text-color-label font-bold"
                    style={{ fontSize: "20px" }}
                  >
                    Date de début
                    <span
                      className="border-1  border-primary-color font-semibold text-black-alpha-90 mt-1"
                      style={{ width: "max-content", padding: "10px 15px" }}
                    >
                      {startFrom?.toLocaleString()}
                    </span>
                  </span>
                </div>
                <div>
                  <span className="span-input-contain">
                    <strong className="pb-3">Horaires hebdomadaires</strong>{" "}
                    {Object.keys(weekSchedule).map((day) => (
                      <div
                        className="col-12 flex flex-column days-week pl-0"
                        key={`unav-${day}-div1`}
                      >
                        <div
                          className="flex flex-row align-items-center"
                          key={`unav-${day}-div1-div1`}
                        >
                          <span
                            className="span-input-contain"
                            style={{
                              width: "-webkit-fill-available",
                              textTransform: "Capitalize",
                            }}
                            key={`unav-${day}-div1-div1-span1`}
                          >
                            <span
                              style={{ width: "84px", marginRight: "15px" }}
                              className="flex flex-nowrap align-items-center"
                            >
                              {day}
                            </span>
                            <span
                              className="border-primary-color p-calendar p-component p-inputwrapper p-calendar-timeonly p-inputwrapper-filled  border-1 justify-content-center font-weight-400-forced"
                              style={{ width: "80px" }}
                            >
                              {weekSchedule[day].debut &&
                                weekSchedule[day].debut.toLocaleTimeString([], {
                                  hour: "2-digit",
                                  minute: "2-digit",
                                })}
                            </span>
                            <span className="separator-hour"></span>
                            <span
                              className="border-primary-color p-calendar p-component p-inputwrapper p-calendar-timeonly p-inputwrapper-filled  border-1 justify-content-center font-weight-400-forced"
                              style={{ width: "80px" }}
                            >
                              {weekSchedule[day].fin &&
                                weekSchedule[day].fin.toLocaleTimeString([], {
                                  hour: "2-digit",
                                  minute: "2-digit",
                                })}
                            </span>
                          </span>
                        </div>
                      </div>
                    ))}
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}
      </Dialog>
      <Toast ref={toast} className="errortest"></Toast>
    </div>
  );
}

{
  /* <div className="mb-5">
              <span className="span-input-contain mt-5">
                <InputTextarea
                  className="inputFW"
                  id="kiosk-adresse"
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                  rows={2}
                  autoResize
                />
                <label htmlFor="kiosk-adresse"> Adresse *</label>
              </span>
            </div> */
}
