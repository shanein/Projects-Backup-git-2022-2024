import React, { useEffect, useState } from "react";
import { InputText, Checkbox, Button } from "primereact";
import { api } from "../../services/config";
// import "../styles/App.scss";
import { useNavigate } from "react-router-dom";
import Logo from "../shared/Logo";
import { sanitizeInput } from "../../services/utils";
import CustomToast from "../shared/CustomToast";
import { useDispatch } from "react-redux";
import { loginUser } from "../../services/store/authSlice";
import { Password } from "primereact/password";

export default function LoginForm({ updateIsAccount }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [checked, setChecked] = useState(false);
  const [showWarning, setShowWarning] = useState(false);
  const [showErr, setShowErr] = useState(false);
  const [warningTXT, setWarningTXT] = useState(false);

  const navigate = useNavigate();
  const dispatch = useDispatch();

  const handleSubmit = (event) => {
    event.preventDefault();
    callLogin();
  };

  const handleChange = () => {
    updateIsAccount(false);
  };

  async function callLogin() {
    const headers = {};
    const body = {
      email: sanitizeInput(email),
      password: sanitizeInput(password),
    };
    try {
      const resp = await api.post("/auth/login", body, { headers });
      if (resp.status === 200) {
        dispatch(
          loginUser({
            user: resp.data.user,
            token: resp.data.token,
          })
        );
        navigate("/home");
      }
    } catch (error) {
      console.error(error);
      if (error.status == 422) {
        setWarningTXT("Utilisateur ou mot de passe incorrect.");
        setShowWarning(true);
      } else {
        // setWarningTXT(
        //   "Une erreur est survenue. Veuillez modifier vos informations de connexion et réessayer."
        // );
        setWarningTXT("Utilisateur ou mot de passe incorrect.");
        setShowWarning(true);
      }
    }
  }

  useEffect(() => {
    setTimeout(() => {
      setShowWarning(false);
    }, 500);
  }, [showWarning]);

  return (
    <div className="flex align-items-center justify-content-center">
      <div className="surface-card p-4 border-round w-full lg:w-6 border-component">
        <div className="text-center mb-5">
          {/* <Logo width={150} height={150} /> */}
          <Logo />
          <div className="text-900 text-3xl font-medium mb-3">
            Accéder à Smart Display
          </div>
          <span className="text-600 font-medium line-height-3">
            Pas encore de compte?
          </span>
          <span
            as="a"
            className="font-medium no-underline ml-2 text-blue-500 cursor-pointer"
            onClick={handleChange}
          >
            Crées-en un!
          </span>
        </div>
        <form onSubmit={handleSubmit}>
          <label htmlFor="email" className="block text-900 font-medium mb-2">
            Email
          </label>
          <InputText
            id="email"
            type="text"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full mb-3"
          />
          <label htmlFor="password" className="block text-900 font-medium mb-2">
            Mot de passe
          </label>
          <Password
            id="password"
            type="password"
            placeholder="Mot de passe"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="passwords-inputs mb-3"
            toggleMask={false}
            feedback={false}
          />
          <div className="flex align-items-center justify-content-between mb-6">
            <div className="flex align-items-center">
              <Checkbox
                id="rememberme"
                onChange={(e) => setChecked(e.checked)}
                checked={checked}
                className="mr-2"
              />
              <label htmlFor="rememberme">Se souvenir de moi</label>
            </div>
            <span
              as="a"
              className="font-medium no-underline ml-2 text-blue-500 text-right cursor-pointer"
            >
              Mot de passe oublié?
            </span>
          </div>
          <Button
            type="submit"
            value="Connexion"
            label="Connexion"
            icon="pi pi-user"
            className="w-full"
          />
        </form>
        <CustomToast
          severity={"warn"}
          title={"Attention"}
          txt={warningTXT}
          display={showWarning}
        />
        <CustomToast
          severity={"error"}
          title={"Erreur"}
          txt={
            "Une erreur est survenue lors du login. \n\n Merci de contacter l'administrateur"
          }
          display={showErr}
        />
      </div>
    </div>
  );
}
