import React, { useRef, useEffect } from "react";
import { Toast } from "primereact";

export default function CustomToast({ severity, title, txt, display }) {
  const toast = useRef(null);

  useEffect(() => {
    if (display === true) {
      toast.current.show({
        severity: severity,
        summary: title,
        detail: txt,
      });
    }
  });

  return (
    <div className="card flex justify-content-center">
      <Toast ref={toast} position="center" />
    </div>
  );
}
