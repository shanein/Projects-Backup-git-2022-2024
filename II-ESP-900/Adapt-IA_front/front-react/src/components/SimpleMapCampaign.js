import React, { useState, useCallback, useEffect } from 'react';
import { GoogleMap, useJsApiLoader, Marker, InfoWindow } from '@react-google-maps/api';

const containerStyle = {
  width: '100%',
  height: '250px'
};

function MapCampaign({ lat, lng, radiusKm, terminals }) {
  const { isLoaded } = useJsApiLoader({
    id: 'google-map-script',
    googleMapsApiKey: "AIzaSyCPrtZUWA8sCCzSlB1F0W6lb0LRv9xi4vY"
  });

  const [map, setMap] = useState(null);
  const [circle, setCircle] = useState(null);
  const [activeMarker, setActiveMarker] = useState(null);

  const onLoad = useCallback(function callback(map) {
    setMap(map);
  }, []);

  const onUnmount = useCallback(function callback() {
    setMap(null);
  }, []);

  useEffect(() => {
    if (circle) {
      circle.setMap(null);
    }

    if (map) {
      const center = { lat, lng };
      const newCircle = new window.google.maps.Circle({
        strokeColor: '#5C69FE',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#5C69FE',
        fillOpacity: 0.35,
        map,
        center: center,
        radius: radiusKm * 1000,
      });

      setCircle(newCircle);

      const bounds = new window.google.maps.LatLngBounds();
      bounds.extend(newCircle.getBounds().getNorthEast());
      bounds.extend(newCircle.getBounds().getSouthWest());
      map.fitBounds(bounds);
    }
  }, [lat, lng, radiusKm, map]);

  const handleMarkerClick = (id) => {
    setActiveMarker(id);
  };

  return isLoaded ? (
    <GoogleMap
      mapContainerStyle={containerStyle}
      center={{ lat, lng }}
      zoom={10}
      onLoad={onLoad}
      onUnmount={onUnmount}
      options={{
        streetViewControl: false,
        mapTypeControl: false,
      }}
    >
      {terminals.map((terminal) => (
        <Marker
          key={terminal.id}
          position={{ lat: terminal.lat, lng: terminal.long }}
          onClick={() => handleMarkerClick(terminal.id)}
        >
          {activeMarker === terminal.id && (
            <InfoWindow onCloseClick={() => setActiveMarker(null)}>
              <div>
                <h3>{terminal.name}</h3>
                <p>{terminal.place_type}</p>
                <p>{terminal.description}</p>
                {/* You can add more details here */}
              </div>
            </InfoWindow>
          )}
        </Marker>
      ))}
    </GoogleMap>
  ) : <></>;
}

export default React.memo(MapCampaign);
