import React, { useState, useEffect } from "react";
import { InputText, Button, Dropdown } from "primereact";
import { api } from "../../services/config";
// import "../styles/App.scss";
// import { useNavigate } from "react-router-dom";
import Logo from "../shared/Logo";
import { sanitizeInput } from "../../services/utils";
import CustomToast from "../shared/CustomToast";
import { RadioButton } from "primereact/radiobutton";
import { Calendar } from "primereact/calendar";
import { InputMask } from "primereact/inputmask";
import { Password } from "primereact/password";
import { Tooltip } from "primereact/tooltip";

export default function RegisterForm({ updateIsAccount }) {
  // const navigate = useNavigate();
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [birthdate, setBirthdate] = useState("");
  const [email, setEmail] = useState("");
  const [phoneNumber, setPhoneNumber] = useState();
  const [companyName, setCompanyName] = useState("");
  const [userType, setUserType] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");

  const [showSuccess, setShowSuccess] = useState(false);
  const [showWarn, setShowWarn] = useState(false);
  const [showError, setShowError] = useState(false);
  const [showPerror, setShowPerror] = useState(false);

  const numb_codes = [
    { name: "+33", code: "+33" },
    { name: "+34", code: "+34" },
    { name: "+32", code: "+32" },
    { name: "+39", code: "+39" },
    { name: "+44", code: "+44" },
  ];

  const [selectedNC, setSelectedNC] = useState(numb_codes[0]);

  const handleChange = () => {
    updateIsAccount(true);
  };

  function cleanDateTime(date) {
    return date.setHours(date.getHours() - date.getTimezoneOffset() / 60);
  }

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (password === password2) {
      const resp = await callRegister();
      resp == true ? handleChange() : <></>;
    } else {
      setShowPerror(true);
    }
  };

  const callRegister = async () => {
    const headers = {
      accept: "application/json",
      "Content-Type": "application/json",
    };
    const body = {
      firstname: sanitizeInput(firstName),
      lastname: sanitizeInput(lastName),
      email: sanitizeInput(email),
      password: sanitizeInput(password),
      // birthdate: birthdate,
      birthdate: cleanDateTime(birthdate),
      // phone_number: selectedNC + phoneNumber,
      phone_number: phoneNumber,
      company_name: sanitizeInput(companyName),
      user_type: userType,
    };

    try {
      const resp = await api.post("/auth/register", body, { headers });
      if (resp.status === 200) {
        setShowSuccess(true);
        return true;
      }
    } catch (error) {
      console.error("error", error);
      if (error.status === 400) {
        setShowWarn(true);
        // showWarn(error.message);
      } else if (error.status === 422) {
        setShowError(true);
        // showWarn(error.message);
      } else if (error.status === 500) {
        setShowError(true);
        // showError(error.message);
      } else {
        console.error(error);
        // showWarn(error.message);
        setShowWarn(true);
      }
      return false;
    }
  };

  useEffect(() => {
    setTimeout(() => {
      setShowWarn(false);
    }, 500);
  }, [showWarn]);

  useEffect(() => {
    setTimeout(() => {
      setShowError(false);
    }, 500);
  }, [showError]);

  useEffect(() => {
    setTimeout(() => {
      setShowSuccess(false);
    }, 500);
  }, [showSuccess]);

  useEffect(() => {
    setTimeout(() => {
      setShowPerror(false);
    }, 500);
  }, [showPerror]);

  return (
    <div className="flex align-items-center justify-content-center">
      <div className="surface-card p-4 border-round w-full lg:w-6 border-component">
        <div className="text-center mb-5">
          {/* <Logo width={150} height={150} /> */}
          <Logo />
          <div className="text-900 text-3xl font-medium mb-3">
            Créer un compte Smart Display
          </div>
          <span className="text-600 font-medium line-height-3">
            Déjà un compte?
          </span>
          <span
            as="a"
            className="font-medium no-underline ml-2 text-blue-500 cursor-pointer"
            onClick={handleChange}
          >
            Connecte-toi!
          </span>
        </div>
        <form onSubmit={handleSubmit} className="">
          <div className="flexRowWrap mt-2 mb-5">
            <span className="p-float-label">
              <InputText
                id="firstName"
                type="text"
                placeholder="Prénom"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                className="w-full"
              />
              <label
                htmlFor="firstName"
                className="block text-900 font-medium mb-2"
              >
                Prénom
              </label>
            </span>

            <span className="p-float-label">
              <InputText
                id="lastName"
                type="text"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                className="w-full "
              />
              <label
                htmlFor="lastName"
                className="block text-900 font-medium mb-3"
              >
                Nom
              </label>
            </span>
          </div>

          <span className="p-float-label  mb-5">
            <InputText
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full"
            />
            <label htmlFor="email" className="block text-900 font-medium mb-2">
              Email
            </label>
          </span>

          <div
            style={{
              display: "flex",
              flexDirection: "row",
              flexWrap: "wrap",
              justifyContent: "space-between",
              alignItems: "stretch",
            }}
            className="mb-5"
          >
            <span
              className="p-float-label"
              style={{ width: "-webkit-fill-available", maxWidth: "45%" }}
            >
              <Calendar
                id="birthdate"
                type="date"
                value={birthdate}
                onChange={(e) => setBirthdate(e.target.value)}
                className="w-full"
                locale="fr"
                dateFormat="dd/mm/yyyy"
                showIcon
              />
              <label
                htmlFor="birthdate"
                className="block text-900 font-medium mb-2"
              >
                Date de naissance
              </label>
            </span>
            <span style={{ width: "-webkit-fill-available", maxWidth: "45%" }}>
              <div className="p-inputgroup flex-1">
                {/* <span className="p-inputgroup-addon ">
                <Dropdown
                  value={selectedNC}
                  onChange={(e) => setSelectedNC(e.value)}
                  options={numb_codes}
                  optionLabel="name"
                  placeholder=""
                  // className="w-full md:w-14rem"
                  className="p-dropdown-sm"
                  style={{ border: "none", backgroundColor: "unset" }}
                />
              </span> */}
                <InputMask
                  id="phoneNumber"
                  type="tel"
                  mask="99 99 99 99 99"
                  placeholder="06 09 02 08 03"
                  value={phoneNumber}
                  onChange={(e) => setPhoneNumber(e.target.value)}
                  // className="w-full mb-3"
                />
                <span className="p-inputgroup-addon">
                  <i className="pi pi-phone"></i>
                </span>
              </div>
            </span>
          </div>

          <div className="mb-5">
            <label
              htmlFor="companyName"
              className="block text-900 font-medium mb-2"
            >
              Nom de l'entreprise
            </label>
            <InputText
              id="companyName"
              type="text"
              placeholder="Entreprise"
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
              className="w-full"
            />
          </div>
          <div className="mb-5">
            <label
              htmlFor="userType"
              className="block text-900 font-medium mb-2"
            >
              Type de compte
            </label>

            <div className="flex flex-row flex-wrap gap-3 align-items-center justify-content-evenly	">
              <div
                className="blc-diff flex align-items-center"
                data-pr-tooltip="Propriétaire de totems ou écrans publicitaires"
              >
                <RadioButton
                  inputId="distributorInput"
                  name="userType"
                  value="distributor"
                  onChange={(e) => setUserType(e.value)}
                  checked={userType === "distributor"}
                  // tooltip="Enter your username"
                  // tooltipOptions={{ position: "bottom" }}
                />
                <label htmlFor="distributorInput" className="ml-2">
                  Diffuseur
                </label>
              </div>
              <Tooltip target=".blc-diff" mouseTrack position="bottom" />
              <div
                className="flex align-items-center blc-diff"
                data-pr-tooltip="Propriétaire de campagnes publicitaires"
              >
                <RadioButton
                  inputId="advertiserInput"
                  name="userType"
                  value="advertiser"
                  onChange={(e) => setUserType(e.value)}
                  checked={userType === "advertiser"}
                />
                <label htmlFor="advertiserInput" className="ml-2">
                  Annonceur
                </label>
              </div>
            </div>
          </div>
          <div className="flexRowWrap my-3">
            <span>
              <label
                htmlFor="password"
                className="block text-900 font-medium mb-2"
              >
                Mot de passe
              </label>
              <Password
                id="password"
                type="password"
                placeholder="Mot de passe"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="mb-3 passwords-inputs"
                toggleMask
              />
            </span>
            <span style={{ width: "-webkit-fill-available", maxWidth: "45%" }}>
              <label
                htmlFor="password2"
                className="block text-900 font-medium mb-2"
              >
                Confirmer le mot de passe
              </label>
              <Password
                id="password2"
                type="password"
                placeholder="Confirmer le mot de passe"
                value={password2}
                onChange={(e) => setPassword2(e.target.value)}
                className="mb-6 passwords-inputs"
                toggleMask
              />
            </span>
          </div>

          <Button
            type="submit"
            value="S'enregistrer"
            label="S'enregistrer"
            icon="pi pi-user"
            className="w-full"
          />
        </form>
        <CustomToast
          severity={"success"}
          title={"Bravo"}
          txt={"Création du compte réussie !"}
          display={showSuccess}
        />
        <CustomToast
          severity={"warn"}
          title={"Attention"}
          txt={"Un compte avec cette adresse email ou username existe déjà"}
          display={showWarn}
        />
        <CustomToast
          severity={"error"}
          title={"Erreur"}
          txt={
            "Une erreur est survenue lors de la création du compte. \n\n Merci de contacter l'administrateur"
          }
          display={showError}
        />
        <CustomToast
          severity={"error"}
          title={"Erreur de forumulaire"}
          txt={"Vos deux password ne correspondent pas !"}
          display={showPerror}
        />
      </div>
    </div>
  );
}
