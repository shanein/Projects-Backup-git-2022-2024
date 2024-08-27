import React from "react";
import { GoogleMap, useJsApiLoader, Marker } from "@react-google-maps/api";

const containerStyle = {
  width: "100%",
  height: "200px",
};

// Modifiez la signature de la fonction pour accepter les props
function Map({ lat, lng, showMarker }) {
  const { isLoaded } = useJsApiLoader({
    id: "google-map-script",
    googleMapsApiKey: "AIzaSyCPrtZUWA8sCCzSlB1F0W6lb0LRv9xi4vY",
  });

  const [map, setMap] = React.useState(null);

  const onLoad = React.useCallback(function callback(map) {
    setMap(map);
  }, []);

  const onUnmount = React.useCallback(function callback(map) {
    setMap(null);
  }, []);

  const center = {
    lat, // Utilisez la prop lat pour la latitude
    lng, // Utilisez la prop lng pour la longitude
  };

  return isLoaded ? (
    <GoogleMap
      mapContainerStyle={containerStyle}
      center={center}
      zoom={12}
      onLoad={onLoad}
      onUnmount={onUnmount}
      options={{
        streetViewControl: false, // Désactive Pegman
        mapTypeControl: false, // Désactive le sélecteur de type de carte
      }}
    >
      {showMarker && <Marker position={{ lat, lng }} />}
    </GoogleMap>
  ) : (
    <></>
  );
}

export default React.memo(Map);
