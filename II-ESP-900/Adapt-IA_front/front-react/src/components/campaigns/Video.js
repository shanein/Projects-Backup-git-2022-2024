import React, { useState, useEffect } from "react";
import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";
import { Dialog } from "primereact/dialog";

// Composant pour afficher la miniature et la vidéo en plein écran
export const VideoThumbnail = ({ videoUrl }) => {
  const [showModal, setShowModal] = useState(false);
  const [thumbnail, setThumbnail] = useState(
    videoUrl.replace("mp4", "jpg").replace("mov", "jpg").replace("avi", "jpg")
  );

  //   useEffect(() => {
  //     generateThumbnail(videoUrl).then((imageDataUrl) => {
  //       setThumbnail(imageDataUrl);
  //     });
  //   }, [videoUrl]);

  const handleThumbnailClick = () => {
    setShowModal(true);
  };

  return (
    <div>
      <img
        src={thumbnail}
        alt="Video Thumbnail"
        onClick={handleThumbnailClick}
        style={{ cursor: "pointer", width: "100px", height: "auto" }}
      />
      {showModal && (
        <Dialog
          header="Video Preview"
          visible={showModal}
          onHide={() => setShowModal(false)}
          modal
        >
          <video width="100%" controls>
            <source src={videoUrl} type="video/mp4" />
            <source src={videoUrl} type="video/mov" />
            Your browser does not support the video tag.
          </video>
        </Dialog>
      )}
    </div>
  );
};

// Fonction pour générer la miniature
export const generateThumbnail = (videoUrl) => {
  return new Promise((resolve, reject) => {
    const video = document.createElement("video");
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");

    video.addEventListener("loadeddata", () => {
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      const imageDataUrl = canvas.toDataURL("image/png");
      resolve(imageDataUrl);
    });

    video.addEventListener("error", () => {
      reject("Error loading video");
    });

    video.src = videoUrl;
    video.load();
  });
};

export const CustomThumbnail = ({ videoFile }) => {
  const [thumbnail, setThumbnail] = useState(null);

  useEffect(() => {
    if (videoFile) {
      const videoUrl = URL.createObjectURL(videoFile);
      const videoElement = document.createElement("video");
      videoElement.src = videoUrl;
      videoElement.crossOrigin = "anonymous";
      videoElement.style.display = "none"; // Cacher l'élément vidéo

      document.body.appendChild(videoElement); // Ajouter l'élément vidéo au DOM

      videoElement.load();
      videoElement.onloadeddata = () => {
        videoElement.currentTime = 1; // Aller à une frame spécifique si nécessaire
      };
      videoElement.onseeked = () => {
        const canvas = document.createElement("canvas");
        canvas.width = videoElement.videoWidth;
        canvas.height = videoElement.videoHeight;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

        canvas.toBlob((blob) => {
          const thumbUrl = URL.createObjectURL(blob);
          setThumbnail(thumbUrl);
          document.body.removeChild(videoElement); // Nettoyer et enlever l'élément vidéo du DOM
        });
      };

      return () => {
        URL.revokeObjectURL(videoUrl);
        if (thumbnail) URL.revokeObjectURL(thumbnail);
      };
    }
  }, [videoFile, thumbnail]);

  return (
    <div>
      {thumbnail && (
        <img
          src={thumbnail}
          alt="Thumbnail"
          style={{ width: "100px", height: "auto" }}
        />
      )}
    </div>
  );
};
