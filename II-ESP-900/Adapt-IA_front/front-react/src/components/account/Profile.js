import React, { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import { api } from "../../services/config";
import { sanitizeInput } from "../../services/utils";
import CustomToast from "../shared/CustomToast";
import { InputText } from "primereact/inputtext";
import { Button } from "primereact/button";
import { InputMask } from "primereact/inputmask";
import { setUser } from "../../services/store/authSlice";
import { useDispatch } from "react-redux";

export default function Profile() {
  const user = useSelector((state) => state.auth.user);
  const dispatch = useDispatch();

  const [userInfo, setUserInfo] = useState({
    id: user.id,
    firstname: user.firstname,
    lastname: user.lastname,
    email: user.email,
    phone_number: user.phone_number,
    user_type: user.user_type,
  });

  const [showSuccess, setShowSuccess] = useState(false);
  const [showWarn, setShowWarn] = useState(false);
  const [showError, setShowError] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setUserInfo((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const resp = await callprofileUpdate();
    if (resp) {
      // Si la mise à jour est réussie, vous pourriez vouloir faire plus ici
    }
  };

  const callprofileUpdate = async () => {
    const headers = {
      accept: "application/json",
      "Content-Type": "application/json",
    };

    const fieldsToUpdate = {};
    if (userInfo.firstname !== user.firstname) {
      fieldsToUpdate.firstname = sanitizeInput(userInfo.firstname);
    }
    if (userInfo.lastname !== user.lastname) {
      fieldsToUpdate.lastname = sanitizeInput(userInfo.lastname);
    }
    if (userInfo.phone_number !== user.phone_number) {
      fieldsToUpdate.phone_number = userInfo.phone_number;
    }

    if (Object.keys(fieldsToUpdate).length === 0) {
      return false;
    }

    try {
      const resp = await api.patch(
        `/auth/update/${userInfo.id}`,
        fieldsToUpdate,
        { headers }
      );
      // const resp = { status: 200 }; // Pour les tests
      // console.log("fieldsToUpdate", fieldsToUpdate);
      // console.log("resp", resp);
      if (resp.status === 200) {
        setShowSuccess(true);
        dispatch(setUser({ user: { ...user, ...fieldsToUpdate } }));
        return true;
      }
    } catch (error) {
      console.error("error", error);
      setShowWarn(true);
      return false;
    }
  };

  useEffect(() => {
    setTimeout(() => {
      setShowWarn(false);
    }, 5000);
  }, [showWarn]);

  useEffect(() => {
    setTimeout(() => {
      setShowError(false);
    }, 5000);
  }, [showError]);

  useEffect(() => {
    setTimeout(() => {
      setShowSuccess(false);
    }, 5000);
  }, [showSuccess]);

  return (
    <div>
      <h2>Profil de l'utilisateur</h2>
      <p>
        Type de compte :{" "}
        <strong>
          {userInfo.user_type === "distributor"
            ? "Propriétaire de terminal"
            : "Publicitaire"}
        </strong>
      </p>
      <p className="mb-5">
        Email : <strong>{userInfo.email}</strong>
      </p>
      <form onSubmit={handleSubmit}>
        <span className="p-float-label mb-5">
          <InputText
            name="firstname"
            value={userInfo.firstname}
            onChange={handleChange}
          />
          <label
            htmlFor="firstname"
            className="block text-900 font-medium mb-3"
          >
            Prénom
          </label>
        </span>
        <span className="p-float-label mb-5">
          <InputText
            name="lastname"
            value={userInfo.lastname}
            onChange={handleChange}
          />
          <label htmlFor="lastname" className="block text-900 font-medium mb-3">
            Nom
          </label>
        </span>
        <span className="p-float-label mb-5">
          <InputMask
            id="phone_number"
            mask="09 99 99 99 99"
            value={userInfo.phone_number}
            onChange={(e) =>
              setUserInfo({ ...userInfo, phone_number: e.value })
            }
          />
          <label
            htmlFor="phone_number"
            className="block text-900 font-medium mb-3"
          >
            Téléphone
          </label>
        </span>
        {hasChanges() && <Button label="Mettre à jour" />}
      </form>
      <CustomToast
        severity={"success"}
        title={"Bravo"}
        txt={"Modification du compte réussie !"}
        display={showSuccess}
      />
      <CustomToast
        severity={"error"}
        title={"Erreur"}
        txt={
          "Une erreur est survenue lors de la mise à jour du compte. Merci de contacter l'administrateur"
        }
        display={showError}
      />
    </div>
  );

  function hasChanges() {
    return (
      userInfo.firstname !== user.firstname ||
      userInfo.lastname !== user.lastname ||
      userInfo.phone_number !== user.phone_number
    );
  }
}
