import React from "react";
import { useSelector } from "react-redux";
import { Outlet, Navigate } from "react-router-dom";
import { useLocation } from "react-router-dom";

const PrivateRoutes = () => {
  const { user, token } = useSelector((state) => state.auth);
  const location = useLocation();

  if (user && token) {
    if (
      !user.is_superuser &&
      user.user_type === "distributor" &&
      (/^\/campaign(\/.+)?$/.test(location.pathname) ||
        location.pathname === "/campaigns")
    ) {
      return <Navigate to="/kiosks" />;
    } else if (
      !user.is_superuser &&
      user.user_type === "advertiser" &&
      (/^\/kiosk(\/.+)?$/.test(location.pathname) ||
        location.pathname === "/kiosks")
    ) {
      return <Navigate to="/campaigns" />;
    }
    return <Outlet />;
  }
  return <Navigate to="/auth" />;
};

export default PrivateRoutes;
