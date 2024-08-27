import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import LoginForm from "../components/auth/LoginForm";
import RegisterForm from "../components/auth/RegisterForm";
import "../styles/auth.scss";
import { useSelector } from "react-redux";

export default function Auth({ status }) {
  const navigate = useNavigate();
  const user = useSelector((state) => state.auth.user);
  const [isAccount, setIsAccount] = useState(status || true);

  const updateIsAccount = (value) => {
    setIsAccount(value);
  };

  useEffect(() => {
    if (user) {
      navigate("/home");
    }
  }, [user, navigate]);

  return (
    <div className="authPage">
      {isAccount ? (
        <LoginForm updateIsAccount={updateIsAccount} />
      ) : (
        <RegisterForm updateIsAccount={updateIsAccount} />
      )}
    </div>
  );
}
