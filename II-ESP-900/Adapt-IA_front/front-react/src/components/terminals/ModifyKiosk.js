import React from "react";
import { Sidebar } from "primereact/sidebar";

export default function ModifyKiosk({
  showModifySlider,
  setShowModifySlider,
  modifyContent,
  setModifyContent,
}) {
  return (
    <>
      <Sidebar
        position="right"
        visible={showModifySlider}
        onHide={() => {
          setShowModifySlider(false);
          setModifyContent({});
        }}
      >
        <h4>{modifyContent?.name}</h4>
        <p>{modifyContent?.description}</p>
      </Sidebar>
    </>
  );
}
