import "./styles/App.scss";
import "./styles/Global.scss";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import React, { Suspense, lazy, useEffect } from "react";
import { PrimeReactProvider } from "primereact/api";
import { ProgressSpinner } from "primereact/progressspinner";
import "primereact/resources/themes/lara-light-blue/theme.css";
import "primereact/resources/primereact.min.css";
import "primeflex/primeflex.css";
import "primeicons/primeicons.css";
import PrivateRoutes from "./services/privateRoutes";
import { useDispatch, useSelector } from "react-redux";
import { logoutUser } from "./services/store/authSlice";
import { addLocale } from "primereact/api";
import { api } from "./services/config";
import TerminalPage from "./components/terminals/TerminalPage";
import Generic from "./views/Generic";
import Campaigns from "./components/Campaigns";
import Account from "./components/Account";
import Dashboard from "./components/Dashboard";
import TerminalPage2 from "./components/terminals/TerminalPage_2";
import Terminals from "./components/Terminals";
import {
  dayNames,
  dayNamesMin,
  dayNamesShort,
  monthNames,
  monthNamesShort,
} from "./services/utils";
import AdPage2 from "./components/campaigns/AdPage2";

const OnePage = lazy(() => import("./views/OnePage"));
const Auth = lazy(() => import("./views/Auth"));
const Home = lazy(() => import("./views/Home"));
const Terminals2 = lazy(() => import("./components/Terminals_2"));

const App = () => {
  const dispatch = useDispatch();
  const lastLogin = useSelector((state) => state.auth.lastLogin);
  const sessionTimeout = 5 * 60 * 1000; // 5 min en ms

  addLocale("fr", {
    firstDayOfWeek: 1,
    showMonthAfterYear: true,
    dayNames: dayNames,
    dayNamesShort: dayNamesShort,
    dayNamesMin: dayNamesMin,
    monthNames: monthNames,
    monthNamesShort: monthNamesShort,
    today: "Aujourd'hui",
    clear: "Clear",
    dateFormat: "dd/mm/yyyy",
    weekHeader: "J",
  });

  useEffect(() => {
    // Fonction pour vérifier la validité de la session
    const checkSession = async () => {
      if (lastLogin && Date.now() - lastLogin > sessionTimeout) {
        try {
          const validT = await api.get("/auth/test");
        } catch (error) {
          dispatch(logoutUser());
        }
      }
    };
    // Vérif si session toujours valide
    checkSession();
    // Vérif session toutes les 5 minutes
    const intervalId = setInterval(checkSession, sessionTimeout);
    // Nettoyer a intervalle lors du démontage du composant
    return () => clearInterval(intervalId);
  }, [dispatch, lastLogin, sessionTimeout]);

  return (
    <PrimeReactProvider>
      <Router>
        <Suspense
          fallback={
            <div>
              <ProgressSpinner />
            </div>
          }
        >
          <Routes>
            <Route path="/" element={<OnePage />} />
            <Route exact path="/auth" element={<Auth />} />
            <Route path="/" element={<PrivateRoutes />}>
              {/* <Route path="home" element={<Home />} /> */}
              <Route
                path="home"
                element={<Generic component={<Dashboard />} />}
              />
              {/* <Route
                path="kiosks"
                element={<Generic component={<Terminals2 />} />}
              /> */}
              <Route
                path="kiosks"
                element={<Generic component={<Terminals />} />}
              />
              <Route
                path="kiosk/:id"
                element={<Generic component={<TerminalPage2 />} />}
              />
              <Route
                path="campaigns"
                element={<Generic component={<Campaigns />} />}
              />
              <Route
                path="campaign/:id"
                element={<Generic component={<AdPage2 />} />}
              />
              <Route
                path="account"
                element={<Generic component={<Account />} />}
              />
              {/* <Route path="kiosk/:id" element={<TerminalPage />} /> */}
              {/* <Route path="kiosks" element={<Terminals />} /> */}
              {/* <Route path="ads" element={<Campaigns />} /> */}
              {/* <Route path="account" element={<Account />} /> */}
            </Route>
          </Routes>
        </Suspense>
      </Router>
    </PrimeReactProvider>
  );
};

export default App;
