import React, { useCallback, useEffect, useRef, useState } from "react";
import { Dialog } from "primereact/dialog";
import { Button } from "primereact/button";
import { ProgressBar } from "primereact/progressbar";
import { InputText } from "primereact/inputtext";
import { InputTextarea } from "primereact/inputtextarea";
import { AutoComplete } from "primereact/autocomplete";
import { InputNumber } from "primereact/inputnumber";
import { Calendar } from "primereact/calendar";
import { FileUpload } from "primereact/fileupload";
import { Tooltip } from "primereact/tooltip";
import { Tag } from "primereact/tag";
import { Toast } from "primereact/toast";
import { Checkbox } from "primereact/checkbox";
import { addAds } from "../../services/store/adsSlice";
import { updateAds } from "../../services/store/adsSlice";
import { deleteVideoUrl } from "../../services/store/adsSlice";
import SimpleMap from "../SimpleMapCampaign";
import ReactPlayer from "react-player";
import { ProgressSpinner } from "primereact/progressspinner";
import { apiService } from "../../services/ApiService";
import { useDispatch } from "react-redux";

import _ from "lodash";

import { api } from "../../services/config";
import { PopUp } from "../../styles/PopUp.scss";

import axios from "axios";
import { CustomThumbnail, VideoThumbnail } from "./Video";

export default function NewCampaign({
  showCreateModal,
  setShowCreateModal,
  campaign,
  setAtSelected,
}) {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const toastGlobal = useRef(null);

  const [name, setName] = useState("");
  const [details, setDetails] = useState("");
  const [address, setAddress] = useState("");
  const [postal_code, setPostalCode] = useState("");
  const [lat, setLat] = useState(48.85837); // Valeur initiale pour la latitude
  const [lng, setLng] = useState(2.294481);
  const [filteredAddresses, setFilteredAddresses] = useState([]);
  const [addressSelected, setAddressSelected] = useState("");
  const [radius, setRadius] = useState(1);
  const [dateRange, setDateRange] = useState("");

  const [showModal, setShowModal] = useState(1);
  const [campaignType, setCampaignType] = useState("");

  const [totalSize, setTotalSize] = useState(0);
  const maxFileSize = 100000000;

  const fileUploadRef = useRef(null);
  const [fileUploaded, setFileUploaded] = useState(false);
  var [file, setFile] = useState(undefined);

  const [campIAPrice, setCampIAPrice] = useState(0);
  const [campClassicPrice, setCampClassicPrice] = useState(0);

  const [terminalsInArea, setTerminalsInArea] = useState([]);

  const [showVideoComponent, setShowVideoComponent] = useState(false);

  const [targets, setTargets] = useState([
    {
      age: [18, 25, 30],
      genre: "male",
    },
  ]);
  const [targetAge, setTargetAge] = useState([]);
  const [sexe, setSexe] = useState(undefined);

  const [progress, setProgress] = useState(0);

  const prices = ["50", "100", "200", "500", "750", "1000", "1500", "2000"];

  const [formData, setFormData] = useState(new FormData());

  const [loading, setLoading] = useState(false);

  const deleteVideoByVideoUrl = (videoUrl) => {
    apiService.deleteVideoByVideoUrl(campaign.videoUrl).then((resp) => {
      if (resp.code == 200) {
        setFileUploaded(false);
        setShowVideoComponent(false);
        dispatch(deleteVideoUrl(campaign.videoUrl));
      }
    });
  };

  function checkInputsModal(index) {
    let nextModal = true;

    switch (index) {
      case 2:
        const cases = [
          { name: "name", value: name },
          { name: "details", value: details },
          { name: "address", value: address },
          { name: "radius", value: radius },
        ];
        cases.forEach((c) => {
          if (!c.value) {
            if (c.name === "address") {
              document
                .getElementById(`camp_address_input`)
                .classList.add("p-invalid");
            } else {
              document
                .getElementById(`camp-${c.name}`)
                .classList.add("p-invalid");
            }
            nextModal = false;
          } else {
            if (c.name === "address") {
              document
                .getElementById(`camp_address_input`)
                .classList.contains("p-invalid") ? (
                document
                  .getElementById(`camp_address_input`)
                  .classList.remove("p-invalid")
              ) : (
                <></>
              );
            } else {
              document
                .getElementById(`camp-${c.name}`)
                .classList.contains("p-invalid") ? (
                document
                  .getElementById(`camp-${c.name}`)
                  .classList.remove("p-invalid")
              ) : (
                <></>
              );
            }
          }
        });
        break;
      case 3:
        console.log("case 3");
        break;
      case 4:
        console.log("case 4");
        if (campaignType === "Classic") {
          if (
            !dateRange ||
            dateRange.length < 1 ||
            dateRange == "" ||
            !dateRange[0] ||
            !dateRange[1]
          ) {
            document
              .getElementById(`camp-daterange-show`)
              .classList.add("p-invalid");
            nextModal = false;
          } else {
            document
              .getElementById(`camp-daterange-show`)
              .classList.contains("p-invalid") ? (
              document
                .getElementById(`camp-daterange-show`)
                .classList.remove("p-invalid")
            ) : (
              <></>
            );
          }
        } else if (campaignType === "IA") {
          if (!campIAPrice || campIAPrice === 0) {
            document.getElementById(`camp-ia-price`).classList.add("p-invalid");
            nextModal = false;
          } else {
            document
              .getElementById(`camp-ia-price`)
              .classList.contains("p-invalid") ? (
              document
                .getElementById(`camp-ia-price`)
                .classList.remove("p-invalid")
            ) : (
              <></>
            );
          }

          if (
            !dateRange ||
            dateRange.length < 1 ||
            dateRange == "" ||
            !dateRange[0] ||
            !dateRange[1]
          ) {
            document
              .getElementById(`camp-daterange-show`)
              .classList.add("p-invalid");
            nextModal = false;
          } else {
            document
              .getElementById(`camp-daterange-show`)
              .classList.contains("p-invalid") ? (
              document
                .getElementById(`camp-daterange-show`)
                .classList.remove("p-invalid")
            ) : (
              <></>
            );
          }
        }
        break;
      case 5:
        if (
          !totalSize ||
          totalSize === 0 ||
          !fileUploadRef ||
          campaign.videoUrl === undefined ||
          campaign.videoUrl === null
        ) {
          setFileUploaded(true);
        } else {
          toast.current.show({
            severity: "error",
            summary: "Error",
            detail: "Please select a file.",
          });
          setFileUploaded(false);
          nextModal = false;
        }
        break;
      default:
        break;
    }

    return nextModal;
  }

  function incrementModal() {
    if (checkInputsModal(showModal)) {
      if (showModal === 2 && campaignType === "Classic") {
        setShowModal(4);
        setProgress(progress + 40);
      } else {
        setShowModal(showModal + 1);
        setProgress(progress + 20);
      }
    }
  }

  function decrementModal() {
    if (showModal === 2) {
      setCampaignType("");
    } else if (showModal === 4 && campaignType === "Classic") {
      setShowModal(2);
      setProgress(progress - 40);
      return;
    }
    setShowModal(showModal - 1);
    setProgress(progress - 20);
  }

  // Méthode pour mettre à jour l'adresse et les coordonnées
  const handleAddressChange = (e) => {
    setAddress(e.value); // Met à jour l'adresse
    if (e.value.lat && e.value.lon) {
      setLat(parseFloat(e.value.lat)); // Met à jour la latitude
      setLng(parseFloat(e.value.lon)); // Met à jour la longitude
    }
  };

  const searchAddress = async (query) => {
    if (typeof query !== "string" || !query.trim()) return;

    try {
      const { data } = await axios.get(
        `https://nominatim.openstreetmap.org/search?addressdetails=1&q=${query}&format=json&countrycodes=fr`
      );
      setFilteredAddresses(data);
    } catch (error) {
      console.error("Error while fetching addresses:", error);
      // alert("Error while fetching addresses. Refresh the page.");
      toastGlobal.current.show({
        severity: "error",
        summary: "Error",
        detail: "Error while fetching addresses. Refresh the page.",
      });
    }
  };
  const debouncedSearchAddress = useCallback(
    _.debounce(searchAddress, 500),
    []
  );

  async function GetTerminalInArea() {
    const url = `/terminals-in-radius/${address.lat}/${address.lon}/${
      radius * 1000
    }`;
    try {
      const kiosks = await api.get(url);

      setTerminalsInArea(kiosks.data);
    } catch (error) {
      console.error("Error while fetching terminals:", error);
      // alert("Error while fetching terminals. Refresh the page.");
      toastGlobal.current.show({
        severity: "error",
        summary: "Error",
        detail:
          "Error while fetching kiosks in area. Refresh the page or ignore this feature.",
      });
      //
    }
  }

  async function PostNewCampaign() {
    setLoading(true);
    formData.set("name", name);
    formData.set("description", details);
    formData.set("start_date", dateRange[0]);
    formData.set("end_date", dateRange[1]);
    campClassicPrice != 0
      ? formData.set("budget", campClassicPrice)
      : formData.set("budget", campIAPrice);
    campClassicPrice != 0
      ? formData.set("is_smart", false)
      : formData.set("is_smart", true);
    formData.set("address", address.display_name);
    formData.set("postal_code", address.address.postcode);
    formData.set("video_file", file);
    formData.set(
      "terminals",
      terminalsInArea.map((t) => t.id)
    );
    formData.set("cibles_json", `[{"age":[${targetAge}], "genre":"${sexe}"}]`);

    const url = "/campaigns/";
    try {
      const newCampaign = await api.post(url, formData, { timeout: 5000 });
      if (newCampaign.status === 200) {
        dispatch(addAds(newCampaign.data));
        setLoading(false);
        setShowCreateModal(false);
        toastGlobal.current.show({
          severity: "success",
          summary: "Success",
          detail: "Campaign successfully created !",
        });

        return newCampaign.data;
      }
    } catch (error) {
      console.error("Error while fetching terminals:", error);
      setLoading(false);
      toastGlobal.current.show({
        severity: "error",
        summary: "Error",
        detail:
          "Error while fetching kiosks in area. Refresh the page or ignore this feature.",
      });
      //
    }
  }

  async function GetClassicPrice(e) {
    if (e.length > 0 && e[0] != e[1] && e[1]) {
      const url = `/campaigns/price/?address=${address.display_name}&start_date=${e[0]}&end_date=${e[1]}`;
      try {
        const duree = e[1] - e[0];
        const differenceInSeconds = duree / 1000;
        const differenceInMinutes = differenceInSeconds / 60;
        const differenceInHours = differenceInMinutes / 60;
        const differenceInDays = differenceInHours / 24;
        const finalPrice = (differenceInDays + 1) * 15;
        setCampClassicPrice(finalPrice);
      } catch (error) {
        console.error("Error while fetching terminals:", error);
        // alert("Error while fetching terminals. Refresh the page.");
        toastGlobal.current.show({
          severity: "error",
          summary: "Error",
          detail:
            "Error while fetching kiosks in area. Refresh the page or ignore this feature.",
        });
        //
      }
    }
  }

  const reInit = () => {
    setShowCreateModal(false);
  };

  // UPLOAD PART
  const onTemplateSelect = (e) => {
    const selectedFile = e.files[0]; // Assuming you're only allowing single file upload

    if (selectedFile instanceof File) {
      // If the selected file is an actual file, not a URL
      let _totalSize = totalSize;
      Object.keys(e.files).forEach((key) => {
        _totalSize += e.files[key].size || 0;
      });
      setTotalSize(_totalSize);
      setFileUploaded(selectedFile);
      setFile(selectedFile);
    } else if (typeof selectedFile === "string") {
      setFileUploaded(true);
      setFile(selectedFile);
    }
  };

  const onTemplateUpload = (e) => {
    let _totalSize = 0;
    e.files.forEach((file) => {
      _totalSize += file.size || 0;
    });
    setTotalSize(_totalSize);
    toast.current.show({
      severity: "info",
      summary: "Success",
      detail: "File Uploaded",
    });

    setFileUploaded(e.files[0]);
  };

  const onTemplateRemove = (file, callback) => {
    setTotalSize(totalSize - file.size);
    setFileUploaded(false);
    setFile(undefined);
    callback();
  };

  const onTemplateClear = () => {
    setTotalSize(0);
  };

  const headerTemplate = (options) => {
    const { className, chooseButton, uploadButton, cancelButton } = options;
    const value = totalSize / maxFileSize;
    const formatedValue =
      fileUploadRef && fileUploadRef.current
        ? fileUploadRef.current.formatSize(totalSize)
        : "0 B";

    return (
      <div
        className={className}
        style={{
          backgroundColor: "transparent",
          display: "flex",
          alignItems: "center",
        }}
      >
        {!file ? chooseButton : <></>}
        {/* {uploadButton} */}
        {/* {cancelButton} */}
        <div className="flex align-items-center gap-3 ml-auto">
          <span>
            {formatedValue} / {maxFileSize / 1000000} MB
          </span>
          <ProgressBar
            value={value}
            showValue={false}
            style={{ width: "10rem", height: "12px" }}
          ></ProgressBar>
        </div>
      </div>
    );
  };

  const itemTemplate = (file, props) => {
    return (
      <div className="flex align-items-center flex-wrap">
        <div className="flex align-items-center" style={{ minWidth: "40%" }}>
          {/* <img
            alt={file.name}
            role="presentation"
            src={campaign ? campaign.videoUrl : file.objectURL}
            width={100}
          /> */}
          {/* <CustomThumbnail videoFile={file} /> */}
          <span className="flex flex-column text-left ml-3">
            {file.name}
            <small>{new Date().toLocaleDateString()}</small>
          </span>
        </div>
        <Tag
          value={props.formatSize}
          severity="warning"
          className="px-3 py-2 mx-4"
        />
        <Button
          type="button"
          icon="pi pi-times"
          className="p-button-outlined p-button-rounded p-button-danger ml-auto"
          onClick={() => onTemplateRemove(file, props.onRemove)}
        />
      </div>
    );
  };

  const emptyTemplate = () => {
    return (
      <div className="flex align-items-center flex-column">
        <i
          className="pi pi-image mt-3 p-5"
          style={{
            fontSize: "5em",
            borderRadius: "50%",
            backgroundColor: "var(--surface-b)",
            color: "var(--surface-d)",
          }}
        ></i>
        <span
          style={{ fontSize: "1.2em", color: "var(--text-color-secondary)" }}
          className="my-5"
        >
          Drag and Drop Image Here
        </span>
      </div>
    );
  };

  const chooseOptions = {
    icon: "pi pi-fw pi-images",
    iconOnly: true,
    className: "custom-choose-btn p-button-rounded p-button-outlined",
  };
  const uploadOptions = {
    icon: "pi pi-fw pi-cloud-upload",
    iconOnly: true,
    className:
      "custom-upload-btn p-button-success p-button-rounded p-button-outlined",
  };
  const cancelOptions = {
    icon: "pi pi-fw pi-times",
    iconOnly: true,
    className:
      "custom-cancel-btn p-button-danger p-button-rounded p-button-outlined",
  };

  // END UPLOAD PART

  const handleClick = (event) => {
    event.preventDefault(); // This prevents the default form submission behavior
    // Your click handling logic here
  };

  const footerContent = (
    <>
      <div className="points-footer">
        <div className="p-d-flex p-jc-center">
          {[...Array(6)].map((_, index) => {
            // Ignorer la modal 3 si campaignType est "Classic"
            if (campaignType === "Classic" && index === 2) return null;
            if (showModal != 1)
              return (
                <div
                  key={index}
                  className={`point ${showModal === index + 1 ? "active" : ""}`}
                ></div>
              );
          })}
        </div>
      </div>
      <div>
        <div className="button-footer">
          {campaign && showModal > 1 ? (
            <Button
              label="Brouillon"
              className="btn-secondary"
              onClick={() => {
                let budget = 0; // Utiliser let au lieu de var pour la portée de bloc
                let is_smart = false; // Utiliser let au lieu de var pour la portée de bloc

                if (campaignType == "IA") {
                  budget = campClassicPrice; // Changed comma to a semicolon
                  is_smart = true; // Added a semicolon
                } else {
                  budget = campIAPrice; // Changed comma to a semicolon
                  is_smart = false; // Added a semicolon
                }
                if (Object.keys(campaign).length != 0) {
                  if (campaign.budget > 0) {
                    budget = campaign.budget;
                  }
                  if (campaign.videoUrl != null) {
                    file = campaign.videoUrl;
                  }
                  apiService
                    .updateDraftCampaign(
                      campaign.id,
                      name,
                      details,
                      dateRange[0],
                      dateRange[1],
                      budget,
                      is_smart,
                      address,
                      postal_code,
                      JSON.stringify([]),
                      file
                    )
                    .then((resp) => {
                      if (resp) {
                        console.log("Broullon Sauvegarder update ");
                        console.log("Response du broullon", resp);
                        setShowCreateModal(false);
                        dispatch(updateAds(resp));
                        setAtSelected(resp);
                      }
                    });
                } else {
                  if (address != "") {
                    apiService
                      .PostDraftCampaign(
                        name,
                        details,
                        dateRange[0],
                        dateRange[1],
                        budget,
                        is_smart,
                        address.display_name,
                        address.address.postcode,
                        JSON.stringify([]),
                        file
                      )
                      .then((resp) => {
                        if (resp) {
                          setShowCreateModal(false);
                          dispatch(updateAds(resp));
                        }
                      });
                  } else {
                    apiService
                      .PostDraftCampaign(
                        name,
                        details,
                        dateRange[0],
                        dateRange[1],
                        budget,
                        is_smart,
                        address,
                        postal_code,
                        JSON.stringify([]),
                        file
                      )
                      .then((resp) => {
                        if (resp) {
                          setShowCreateModal(false);
                          dispatch(updateAds(resp));
                        }
                      });
                  }
                }
              }}
              autoFocus
            />
          ) : (
            <></>
          )}
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
          {showModal > 1 && showModal < 6 ? (
            <Button
              label="Suivant"
              onClick={() => incrementModal()}
              autoFocus
              className="btn-primary"
            />
          ) : (
            <></>
          )}
          {showModal == 6 ? (
            <Button
              label="Souvegarder"
              icon="pi pi-check"
              onClick={() => {
                let budget = 0; // Use let instead of var for block-scoping
                let is_smart = false; // Use let instead of var for block-scoping

                campaignType == "IA"
                  ? (budget = campClassicPrice)
                  : (budget = campIAPrice);
                campaignType == "IA" ? (is_smart = true) : (is_smart = false);

                if (Object.keys(campaign).length != 0) {
                  apiService
                    .updateDraftCampaign(
                      campaign.id,
                      name,
                      details,
                      dateRange[0],
                      dateRange[1],
                      budget,
                      is_smart,
                      address,
                      postal_code,
                      JSON.stringify([]),
                      file
                    )
                    .then((resp) => {
                      if (resp) {
                        apiService
                          .updateDraftCampaignStatus(resp.id, true)
                          .then(() => {
                            // Mettre à jour le statut de la campagne réussie
                            setShowCreateModal(false);

                            dispatch(updateAds(resp));
                          })
                          .catch((error) => {
                            // Gérer les erreurs lors de la mise à jour du statut de la campagne
                            console.error(
                              "Erreur lors de la mise à jour du statut de la campagne :",
                              error
                            );
                          });
                      }
                    });
                } else {
                  apiService
                    .PostDraftCampaign(
                      name,
                      details,
                      dateRange[0],
                      dateRange[1],
                      budget,
                      is_smart,
                      address.display_name,
                      address.address.postcode,
                      JSON.stringify([]),
                      file
                    )
                    .then((resp) => {
                      if (resp) {
                        apiService
                          .updateDraftCampaignStatus(resp[0].id, true)
                          .then(() => {
                            // Mettre à jour le statut de la campagne réussie
                            setShowCreateModal(false);
                            dispatch(updateAds(resp[0]));
                          })
                          .catch((error) => {
                            // Gérer les erreurs lors de la mise à jour du statut de la campagne
                            console.error(
                              "Erreur lors de la mise à jour du statut de la campagne :",
                              error
                            );
                          });
                      }
                    });
                }
              }}
              autoFocus
              className="btn-primary my-2"
            />
          ) : (
            <></>
          )}
        </div>
      </div>
    </>
  );

  const modal2 = (
    <div className="card justify-content-center mt-5 pop-container-centered ">
      <div className="flex flex-wrap justify-content-around">
        <div className="flex flex-column">
          <div className="mb-5">
            <span className="font-bold span-input-contain">
              <label htmlFor="camp-name" className="text-color-label">
                Nom de la Campagne *
              </label>
              <InputText
                id="camp-name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                className="p-inputtext p-component border-1  border-primary-color font-semibold border-1  border-primary-color font-semibold"
              />
            </span>
          </div>
          <div className="mb-5">
            <span className="span-input-contain font-bold">
              <label htmlFor="camp-details" className="text-color-label">
                {" "}
                Description Détaillée *
              </label>
              <InputTextarea
                className="inputFW border-1  border-primary-color font-semibold"
                id="camp-details"
                value={details}
                onChange={(e) => setDetails(e.target.value)}
                rows={2}
                autoResize
                required
              />
            </span>
          </div>
        </div>
        <div className="flex flex-column">
          <div className="mb-5">
            <span className="font-bold span-input-contain">
              <label htmlFor="camp_address_input" className="text-color-label">
                {" "}
                Adresse *
              </label>
              <div className="grid-adresse">
                <AutoComplete
                  className="inputFW p-fluid"
                  inputId="camp_address_input"
                  inputClassName="border-1  border-primary-color font-semibold"
                  value={address.display_name || address}
                  suggestions={filteredAddresses}
                  completeMethod={(e) => {
                    setAddress(e.query);
                    setAddressSelected(e.query);
                  }}
                  field="display_name"
                  onChange={handleAddressChange}
                  required
                />
                <InputNumber
                  inputClassName="border-1  border-primary-color font-semibold"
                  inputId="camp-radius"
                  value={radius}
                  onValueChange={(e) => {
                    setRadius(e.value); // Update radius state
                  }}
                  min={1}
                  max={50}
                  showButtons
                  suffix=" km"
                  required
                />
              </div>
            </span>
            <div className="map-born">
              <SimpleMap
                lat={lat}
                lng={lng}
                radiusKm={radius}
                terminals={terminalsInArea}
              />
            </div>
            {/*<div className="mb-5">*/}
            {/*  <span className="p-float-label mt-5">*/}
            {/*    <InputNumber*/}
            {/*      inputId="camp-radius"*/}
            {/*      value={radius}*/}
            {/*      onValueChange={(e) => {*/}
            {/*        setRadius(e.value); // Update radius state*/}
            {/*      }}*/}
            {/*      min={1}*/}
            {/*      max={50}*/}
            {/*      showButtons*/}
            {/*      suffix=" km"*/}
            {/*      required*/}
            {/*    />*/}
            {/*    <label htmlFor="camp-radius">Radius *</label>*/}
            {/*  </span>*/}
            {/*</div>*/}
            {/*  <div>MAP BLOC</div>*/}
            <div
              className={
                terminalsInArea.length >= 1
                  ? "zone-terminal green-terminal"
                  : "zone-terminal"
              }
            >
              <span>
                {terminalsInArea.length} borne
                {terminalsInArea.length <= 1 ? "" : "s"}{" "}
              </span>
              dans la zone
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const modal3IA = (
    <div>
      <div className="text-color-label font-bold">Cible(s) de la campagne</div>
      <div className="age-list">
        <div className="flex flex-wrap justify-content-center">
          <div className="flex align-items-center text-color-label">Age</div>
          <div className="flex align-items-center">
            <Checkbox
              inputId="age1"
              onChange={(e) => {
                if (targetAge[0] !== 0 || targetAge[1] !== 2) {
                  setTargetAge([0, 2]);
                } else {
                  setTargetAge([]);
                }
              }}
              checked={targetAge[0] == 0 && targetAge[1] == 2 ? true : false}
            />
            <label htmlFor="age1" className="p-checkbox-label">
              Enfants (0-2 ans)
            </label>
          </div>
          <div className="flex align-items-center">
            <Checkbox
              inputId="age2"
              onChange={(e) => {
                e.checked == true ? setTargetAge([4, 6]) : setTargetAge([]);
              }}
              checked={targetAge[0] == 4 && targetAge[1] == 6 ? true : false}
            />
            <label htmlFor="age2" className="p-checkbox-label">
              Enfants (4-6 ans)
            </label>
          </div>
          <div className="flex align-items-center">
            <Checkbox
              inputId="age3"
              onChange={(e) => {
                e.checked == true ? setTargetAge([8, 12]) : setTargetAge([]);
              }}
              checked={targetAge[0] == 8 && targetAge[1] == 12 ? true : false}
            />
            <label htmlFor="age3" className="p-checkbox-label">
              Enfants (8-12 ans)
            </label>
          </div>
          <div className="flex align-items-center">
            <Checkbox
              inputId="age4"
              onChange={(e) => {
                e.checked == true ? setTargetAge([15, 20]) : setTargetAge([]);
              }}
              checked={targetAge[0] == 15 && targetAge[1] == 20 ? true : false}
            />
            <label htmlFor="age4" className="p-checkbox-label">
              Enfants (15-20 ans)
            </label>
          </div>
          <div className="flex align-items-center">
            <Checkbox
              inputId="age5"
              onChange={(e) => {
                e.checked == true ? setTargetAge([25, 32]) : setTargetAge([]);
              }}
              checked={targetAge[0] == 25 && targetAge[1] == 32 ? true : false}
            />
            <label htmlFor="age5" className="p-checkbox-label">
              Enfants (25-32 ans)
            </label>
          </div>
          <div className="flex align-items-center">
            <Checkbox
              inputId="age6"
              onChange={(e) => {
                e.checked == true ? setTargetAge([38, 43]) : setTargetAge([]);
              }}
              checked={targetAge[0] == 38 && targetAge[1] == 43 ? true : false}
            />
            <label htmlFor="age6" className="p-checkbox-label">
              Enfants (38-43 ans)
            </label>
          </div>
          <div className="flex align-items-center">
            <Checkbox
              inputId="age7"
              onChange={(e) => {
                e.checked == true ? setTargetAge([48, 53]) : setTargetAge([]);
              }}
              checked={targetAge[0] == 48 && targetAge[1] == 53 ? true : false}
            />
            <label htmlFor="age7" className="p-checkbox-label">
              Enfants (48-53 ans)
            </label>
          </div>
          <div className="flex align-items-center">
            <Checkbox
              inputId="age8"
              onChange={(e) => {
                e.checked == true ? setTargetAge([60, 100]) : setTargetAge([]);
              }}
              checked={targetAge[0] == 60 && targetAge[1] == 100 ? true : false}
            />
            <label htmlFor="age8" className="p-checkbox-label">
              Enfants (60-100 ans)
            </label>
          </div>
        </div>
        <div className="flex flex-wrap justify-content-center">
          <div className="flex align-items-center text-color-label">Sexe</div>
          <div className="flex align-items-center">
            <Checkbox
              inputId="homme"
              onChange={(e) => {
                e.checked == true ? setSexe("male") : setSexe(undefined);
              }}
              checked={sexe == "male" ? true : false}
            />
            <label htmlFor="homme" className="p-checkbox-label">
              Homme
            </label>
          </div>
          <div className="flex align-items-center">
            <Checkbox
              inputId="femme"
              onChange={(e) => {
                e.checked == true ? setSexe("female") : setSexe(undefined);
              }}
              checked={sexe == "female" ? true : false}
            />
            <label htmlFor="femme" className="p-checkbox-label">
              Femme
            </label>
          </div>
        </div>
      </div>
    </div>
  );

  const modal4IA = (
    <div className="card justify-content-center mt-5  mt-5 pop-container-centered modal-centered">
      <div className="flex flex-wrap justify-content-around">
        <div className="flex flex-column align-items-center">
          <div
            className="text-color-label font-bold"
            style={{ fontSize: "20px" }}
          >
            Budget
          </div>
          <div className="price-text">
            Budget maximum alloué
            <br />
            pour la campagne
          </div>
          <div className="grid-price-ia">
            {prices.map((price) => (
              <Button
                key={price}
                label={`${price}\u00A0€`}
                // className="p-button-text"
                className={`p-button-text ${
                  campIAPrice === price ? "selected-price" : ""
                }`}
                onClick={() => setCampIAPrice(price)}
                style={{ margin: "0 5px" }}
              />
            ))}

            <InputNumber
              inputId="camp-ia-price"
              // value={campIAPrice}
              onValueChange={(e) => setCampIAPrice(e.value)}
              mode="currency"
              currency="EUR"
              locale="fr-FR"
              minFractionDigits={0}
              maxFractionDigits={0}
              placeholder="Entrez un budget"
            />
          </div>
          <div className="mb-5 mt-5 ">
            <div className="price-big">{campIAPrice}&nbsp;€</div>
          </div>
        </div>
        <div className="flex flex-column align-items-center">
          <label
            htmlFor={`camp-daterange`}
            className="text-color-label font-bold"
            style={{ fontSize: "20px" }}
          >
            Date de début et de fin de la campagne *
          </label>
          <span>
            <Calendar
              value={dateRange}
              id={`camp-daterange-show`}
              className="inputFW period-campaign-input"
              selectionMode="range"
              locale="fr"
              readOnlyInput
              showButtonBar
              dateFormat="dd/mm/yy"
              // showTime
              disabled
            />
          </span>
          <span
            className="p-float-label mt-5"
            style={{ width: "-webkit-fill-available" }}
          >
            <Calendar
              value={dateRange}
              id={`camp-daterange`}
              className="inputFW period-campaign"
              onChange={(e) => {
                setDateRange(e.value);
              }}
              minDate={new Date()}
              selectionMode="range"
              dateFormat="dd/mm/yy"
              locale="fr"
              // showIcon
              readOnlyInput
              showButtonBar
              // showTime
              inline
              style={{ borderRadius: "20px" }}
            />
          </span>
        </div>
      </div>
    </div>
  );
  const modal4Classic = (
    <div className="card justify-content-center mt-5 pop-container-centered modal-centered">
      <div className="flex flex-wrap justify-content-around">
        <div className="flex flex-column align-items-center">
          <div
            className="text-color-label font-bold"
            style={{ fontSize: "20px" }}
          >
            Prix
          </div>
          <div className="price-text">
            Prix defini
            <br />
            pour la campagne
          </div>
          <div className="mb-5 mt-5 ">
            <div>
              {/*<div>Price</div>*/}
              <div className="price-big">
                {campClassicPrice ? Math.round(campClassicPrice) : "0"}&nbsp;€
              </div>
            </div>
          </div>
        </div>
        <div className="flex flex-column align-items-center">
          <label
            htmlFor={`camp-daterange`}
            className="text-color-label font-bold"
            style={{ fontSize: "20px" }}
          >
            Date de début et de fin de la campagne*
          </label>
          <span className="">
            <Calendar
              value={dateRange}
              id={`camp-daterange-show`}
              className="inputFW period-campaign-input"
              selectionMode="range"
              locale="fr"
              readOnlyInput
              showButtonBar
              dateFormat="dd/mm/yy"
              // showTime
              disabled
            />
          </span>
          <span
            className="p-float-label  mt-5"
            style={{ width: "-webkit-fill-available" }}
          >
            <Calendar
              value={dateRange}
              id={`camp-daterange`}
              className="inputFW period-campaign"
              onChange={(e) => {
                setDateRange(e.value);
                GetClassicPrice(e.value);
              }}
              minDate={new Date()}
              selectionMode="range"
              dateFormat="dd/mm/yy"
              locale="fr"
              // showIcon
              readOnlyInput
              showButtonBar
              // showTime
              inline
              style={{ borderRadius: "20px" }}
            />
          </span>
        </div>
      </div>
    </div>
  );
  const modal5 = (
    <div className="card justify-content-center mt-5 modal-centered">
      {/*<div className="mb-5 mt-5">modal5</div>*/}
      <div className="mb-5 mt-5">
        <Toast ref={toast}></Toast>

        <Tooltip
          target=".custom-choose-btn"
          content="Choose"
          position="bottom"
        />
        <Tooltip
          target=".custom-upload-btn"
          content="Upload"
          position="bottom"
        />
        <Tooltip
          target=".custom-cancel-btn"
          content="Clear"
          position="bottom"
        />

        {showVideoComponent ? (
          <div
            style={{
              flex: 1,
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <div
              style={{
                position: "relative",
                width: "100%",
                height: "400px",
                border: "2px solid #000000",
                borderRadius: "5px",
                overflow: "hidden",
              }}
            >
              {/* Afficher la vidéo */}
              <video
                src={campaign.videoUrl}
                controls
                style={{ width: "100%", height: "100%" }}
              />

              {/* Bouton "Supprimer la vidéo" */}
              <Button
                icon="pi pi-trash"
                className="p-button-danger"
                style={{
                  position: "absolute",
                  top: "10px",
                  right: "10px",
                  zIndex: 1,
                }}
                severity="danger"
                aria-label="Cancel"
                onClick={() => {
                  apiService
                    .deleteVideoByVideoUrl(campaign.videoUrl)
                    .then((resp) => {
                      if (resp.code == 200) {
                        setFileUploaded(false);
                        setShowVideoComponent(false);
                        dispatch(deleteVideoUrl(campaign.videoUrl));
                      }
                    });
                }}
              />
            </div>
          </div>
        ) : (
          <FileUpload
            ref={fileUploadRef}
            name="video_picker"
            accept="video/*"
            maxFileSize={maxFileSize}
            onUpload={onTemplateUpload}
            onSelect={onTemplateSelect}
            onError={onTemplateClear}
            onClear={onTemplateClear}
            headerTemplate={headerTemplate}
            itemTemplate={itemTemplate}
            emptyTemplate={emptyTemplate}
            chooseOptions={chooseOptions}
            uploadOptions={uploadOptions}
            cancelOptions={cancelOptions}
          />
        )}
      </div>
    </div>
  );

  const modal6IA = (
    <div>
      <div>modal6IA</div>
      <div>Detailled Description for IA Modal 6 Creation IA</div>
      pareil que l autre enfaite
    </div>
  );
  const modal6Classic = (
    <div className="card justify-content-center mt-5">
      <div className="mb-5 mt-5">Résumé de la campagne</div>
      <div className="mb-5 mt-5">
        Name : <span>{name}</span>
      </div>
      <div className="mb-5 mt-5">
        Details : <span>{details}</span>
      </div>
      <div className="mb-5 mt-5">
        Address : <span>{address}</span>
      </div>
      <div className="mb-5 mt-5">
        Radius : <span>{radius}</span>
      </div>
      <div className="mb-5 mt-5"></div>
      <div className="mb-5 mt-5">
        Video : <span>{fileUploaded ? "true" : "false"}</span>
      </div>
      {targets ? (
        <div className="mb-5 mt-5">
          Targets : <span>{fileUploaded}</span>
        </div>
      ) : (
        <></>
      )}
      <div className="mb-5 mt-5">
        Price : <span>{campClassicPrice}</span>
      </div>
    </div>
  );

  const modal6 = (
    <div className="card justify-content-center mt-5">
      <div className="mb-2 mt-5">Résumé de la campagne</div>
      <div className="flex flex-wrap justify-content-around text-color-label mobile-left">
        <div className="flex flex-column md:w-6 left-content-end">
          <div className="mb-3">
            <span className="span-input-contain">
              <strong>Nom : </strong>
              {name}
            </span>
          </div>
          <div className="mb-3">
            <span className="span-input-contain">
              <strong>Description : </strong>
              {details}
            </span>
          </div>
          <div className="mb-3">
           <span className="span-input-contain">
            <strong>Adresse :</strong>
            <span>
            {Object.keys(campaign).length != 0 ? address : ""},
             {address.display_name}
              <strong> +/- {radius}km</strong>
            </span>
          </span>
          </div>
          {targets  > 0 ? (
            <div className="mb-3">
              <strong>Targets :</strong>
              <ul>
                <li>Age: {targets.age}</li>
                <li>Genre: {targets.genre}</li>
              </ul>
            </div>
          ) : (
            <></>
          )}
          {campaignType === "Classic" ? (
            <div className="mb-3">
              <strong>Prix :</strong> <span>{campClassicPrice}</span>
            </div>
                ) : campaignType === "IA" ? (

                  <div className="mb-3">
                    <strong>Budget :</strong> <span>{campIAPrice}</span>
                   </div>) :

                  <></>
                }
          <div className="mb-3">
            <strong>Video :</strong>{" "}
            {showVideoComponent ? (
              <ReactPlayer
                url={campaign.videoUrl}
                width="6O%"
                height="100%"
                controls
                style={{
                  aspectRatio: 1080 / 1920,
                  maxHeight: "300px",
                  margin: "auto",
                }}
              />
            ) : (
              <></>
            )}
          </div>
        </div>
        <div className="flex flex-column md:w-6 align-items-center">
          <label
            htmlFor={`camp-daterange`}
            className="text-color-label font-bold"
            style={{ fontSize: "20px" }}
          >
            Date de début et de fin de la campagne*
          </label>
          <span className="">
            <Calendar
              value={dateRange}
              id={`camp-daterange-show`}
              className="inputFW period-campaign-input"
              selectionMode="range"
              locale="fr"
              readOnlyInput
              showButtonBar
              dateFormat="dd/mm/yy"
              // showTime
              disabled
            />
          </span>
          <span
            className="p-float-label  mt-5"
            style={{ width: "-webkit-fill-available" }}
          >
            <Calendar
              value={dateRange}
              id={`camp-daterange`}
              className="inputFW period-campaign"
              onChange={(e) => {
                setDateRange(e.value);
                if (campaignType === "Classic") {
                  GetClassicPrice(e.value);
                }
              }}
              minDate={new Date()}
              selectionMode="range"
              dateFormat="dd/mm/yy"
              locale="fr"
              // showIcon
              readOnlyInput
              showButtonBar
              // showTime
              inline
              style={{ borderRadius: "20px" }}
            />
          </span>
        </div>
      </div>
    </div>
  );


  useEffect(() => {
    const addressString =
      typeof address === "string" ? address : address?.display_name || "";
    if (addressString.trim()) {
      debouncedSearchAddress(addressString);
    } else {
      setFilteredAddresses([]);
    }
    if (
      (Object.keys(campaign).length != 0
        ? campaign.address
        : address.display_name) &&
      radius > 0
    ) {
      setFile(Object.keys(campaign).length != 0 ? campaign.videoUrl : file);
      //  GetTerminalInArea();
    }
  }, [address, debouncedSearchAddress, radius]);

  useEffect(() => {
    if (Object.keys(campaign).length != 0) {
      setName(campaign.name);
      setDetails(campaign.description);
      setAddress(campaign.address);
      setPostalCode(campaign.postal_code);
      // setRadius(campaign.radius);
      if (campaign.start_date && campaign.end_date) {
        setDateRange([
          Object.keys(campaign).length != 0 && campaign.start_date
            ? new Date(campaign.start_date)
            : null,
          Object.keys(campaign).length != 0 && campaign.end_date
            ? new Date(campaign.end_date)
            : null,
        ]);
      }

      {
        campaign.is_smart
          ? setCampIAPrice(campaign.budget)
          : setCampClassicPrice(campaign.budget);
      }

      if (Object.keys(campaign).length != 0 && campaign.videoUrl) {
        setShowVideoComponent(true);
      }

      console.log("VALUE OF CAMPAIGN VIDEO URL", campaign.videoUrl);
      setFile(campaign.videoUrl);
    }
  }, [campaign]);

  useEffect(() => {
    // Ensure both radius and address are ready
    if (radius && address?.lat && address?.lon) {
      GetTerminalInArea();
    }
  }, [radius, address]);

  return (
    <div className="card flex justify-content-center">
      <Dialog
        header="Créer une nouvelle campagne"
        visible={showCreateModal}
        onHide={reInit}
        footer={footerContent}
        style={{ width: "90vw" }}
        breakpoints={{ "960px": "75vw", "641px": "100vw" }}
        maximizable
        id="new-campaign-modal"
      >
        {showModal === 1 && (
          <div
            style={{
              display: "flex",
              flexDirection: "row",
              justifyContent: "space-evenly",
              flexWrap: "wrap",
              height: "100%",
            }}
          >
            <div
              className="title-choice font-bold mt-auto mb-5"
              style={{ width: "100%", textAlign: "center" }}
            >
              Choisissez le mode de campagne que vous souhaitez créer
            </div>
            <Button
              className="btn-campaign-choice btn-campaign-choice-classic"
              onClick={() => {
                setCampaignType("Classic");
                incrementModal();
              }}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="114"
                height="131"
                viewBox="0 0 114 131"
                fill="none"
              >
                <path
                  d="M99.75 14.5556C107.588 14.5556 114 21.1056 114 29.1111V116.444C114 124.45 107.588 131 99.75 131H14.25C6.41251 131 0 124.45 0 116.444V29.1111C0 21.1056 6.41251 14.5556 14.25 14.5556H37.05C39.9 5.82222 47.7375 0 57 0C66.2625 0 74.1 5.82222 76.95 14.5556H99.75ZM57 14.5556C52.725 14.5556 49.875 18.1944 49.875 21.8333C49.875 25.4722 52.725 29.1111 57 29.1111C61.275 29.1111 64.125 26.2 64.125 21.8333C64.125 17.4667 61.275 14.5556 57 14.5556ZM28.5 43.6667V29.1111H14.25V116.444H99.75V29.1111H85.5V43.6667H28.5ZM42.75 101.889V58.2222L78.375 80.0556"
                  fill="white"
                />
              </svg>
              Campagne classique
            </Button>
            <Button
              className="btn-campaign-choice btn-campaign-choice-ia"
              onClick={() => {
                setCampaignType("IA");
                incrementModal();
              }}
            >
              <svg
                width="208"
                height="93"
                viewBox="0 0 208 93"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M70 10.3333C75.5 10.3333 80 14.9833 80 20.6667V82.6667C80 88.35 75.5 93 70 93H10C4.5 93 0 88.35 0 82.6667V20.6667C0 14.9833 4.5 10.3333 10 10.3333H26C28 4.13333 33.5 0 40 0C46.5 0 52 4.13333 54 10.3333H70ZM40 10.3333C37 10.3333 35 12.9167 35 15.5C35 18.0833 37 20.6667 40 20.6667C43 20.6667 45 18.6 45 15.5C45 12.4 43 10.3333 40 10.3333ZM20 31V20.6667H10V82.6667H70V20.6667H60V31H20ZM30 72.3333V41.3333L55 56.8333"
                  fill="white"
                />
                <path
                  d="M156.381 29.072V74H145.437V29.072H156.381ZM192.28 66.064H175.512L172.824 74H161.368L177.624 29.072H190.296L206.552 74H194.968L192.28 66.064ZM189.464 57.616L183.896 41.168L178.392 57.616H189.464Z"
                  fill="white"
                />
                <path
                  d="M101.892 41L122 61.1077L119.108 64L99 43.8923L101.892 41Z"
                  fill="white"
                />
                <path
                  d="M99.0001 61.1077L119.108 41L122 43.8923L101.892 64L99.0001 61.1077Z"
                  fill="white"
                />
              </svg>
              Campagne avec IA
            </Button>
          </div>
        )}
        {showModal === 2 && modal2}

        {showModal === 3 && campaignType === "IA" && modal3IA}

        {showModal === 4 && campaignType === "IA" && modal4IA}
        {showModal === 4 && campaignType === "Classic" && modal4Classic}

        {showModal === 5 && campaignType && modal5}

        {/* {showModal === 6 && campaignType === "IA" && modal6IA}
        {showModal === 6 && campaignType === "Classic" && modal6Classic} */}

        {showModal === 6 && modal6}
      </Dialog>
      <Toast ref={toastGlobal} style={{ zIndex: 20 }}></Toast>
      {loading ? <ProgressSpinner /> : <></>}
    </div>
  );
}
