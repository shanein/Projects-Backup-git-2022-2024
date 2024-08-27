import React from "react";
import { useSelector, useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { Button } from "primereact/button";
import { useEffect, useState, useRef } from "react";
import { api } from "../../services/config";
import { setKiosks } from "../../services/store/kiosksSlice";
import ModifyKiosk from "./ModifyKiosk";
import { SplitButton } from "primereact/splitbutton";
import { Toast } from "primereact/toast";

// --------- datatable----------------
import { classNames } from 'primereact/utils';
import { FilterMatchMode, FilterOperator } from 'primereact/api';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { InputText } from 'primereact/inputtext';
import { Dropdown } from 'primereact/dropdown';
import { MultiSelect } from 'primereact/multiselect';
import { Tag } from 'primereact/tag';
import { TriStateCheckbox } from 'primereact/tristatecheckbox';
import {ProgressSpinner} from "primereact/progressspinner";
import {Badge} from "primereact/badge";
// -------------------------

export default function KioskTable() {

  const [showModifySlider, setShowModifySlider] = useState(false);
  const terminals = useSelector((state) => state.kiosks.kiosks);
  const [modifyContent, setModifyContent] = useState({});

  const dispatch = useDispatch();
  const toast = useRef(null);
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true)
  const [totalRecords, setTotalRecords] = useState(0);
  const [selectedTerminal, setSelectedTerminal] = useState(null);
  const [selectAll, setSelectAll] = useState(false);


  const statusBody = (rowData, column) => {
    const iconClass = rowData.is_active ? 'pi pi-circle-on  terminalActive' : 'pi pi-circle-on terminalInactive';
    return (
        <div>
          <span  className={iconClass}></span>
        </div>
    );
  };
  const detailsBody = (rowData, column) => {
    return (
        <div className="grid">
          <div className="col-2  kiosk-icon">
            <span className=" ic-size pi pi-server"></span>
          </div>
          <div className="col-10 dt-text">
            <p className="name font-bold">
              <span>{rowData.name}</span>
            </p>
            <p className="place">
              {/*<span className=" pi pi-map-marker"></span>*/}
              <span>{rowData.localisation}</span>
            </p>
            <p className="cstm">
              <span>{"Last ping 1h15"} </span>
            </p>
          </div>

        </div>
    )
  }
  const infosBody = () => {
    return (
        <div className="badge flex">

          <div className="x x1">
            <Badge value="85%" style={{fontSize: "9px", }}></Badge>
            <p>
              Usage
            </p>
          </div>
          <div className="x x2">
            <Badge value="30k €" style={{fontSize: "9px", }}></Badge>
            <p>
              Income
            </p>
          </div>
          <div className="x x3">
            <Badge value="85%" style={{fontSize: "9px", }}></Badge>
            <p>
              Network
            </p>
          </div>

        </div>
    )
  }
  //
  const manBody = ()=>{
    return (
        <>
          <span className="pi pi-cog"></span>
        </>
    )
  }

  // const items = [
  //   // {
  //   //   label: "Informations Update",
  //   //   icon: "pi pi-list",
  //   //   command: () => {
  //   //     // toast.current.show({
  //   //     //   severity: "success",
  //   //     //   summary: "Updated",
  //   //     //   detail: "Data Updated",
  //   //     // });
  //   //     navigate("/kiosk/");
  //   //   },
  //   // },
  //   {
  //     label: "Download Installeur",
  //     icon: "pi pi-download",
  //     command: async () => {
  //       await api.get(`/kiosk/${terminal.id}/download`);
  //     },
  //   },
  //   {
  //     label: "Delete",
  //     icon: "pi pi-times",
  //     command: () => {
  //       toast.current.show({
  //         severity: "warn",
  //         summary: "Delete",
  //         detail: "Data Deleted",
  //       });
  //     },
  //   },
  // ];

  function createItems(terminalId) {
    return [
      {
        label: "Informations Update",
        icon: "pi pi-list",
        command: () => {
          // toast.current.show({
          //   severity: "success",
          //   summary: "Updated",
          //   detail: "Data Updated",
          // });
          navigate(`/kiosk/${terminalId}`);
        },
      },
      {
        label: "Download Installeur",
        icon: "pi pi-download",
        command: async () => {
          await api.get(`/kiosk/${terminalId}/download`);
        },
      },
      {
        label: "Delete",
        icon: "pi pi-times",
        command: () => {
          toast.current.show({
            severity: "warn",
            summary: "Delete",
            detail: "Data Deleted",
          });
        },
      },
    ];
  }

  function navigateToKiosk(event: DataTableSelectionChangeEvent) {
      const id = event.value.id
    navigate(`/kiosk/${id}`);
  }

  return (
      <>
          {
              !terminals ?
              <div className="card flex justify-content-center">
              <ProgressSpinner/>
              </div>
              :
              <DataTable
                  selection={selectedTerminal}
                  selectionMode="single"
                  totalRecords={totalRecords}
                  onSelectionChange={navigateToKiosk}
                  selectAll={selectAll}
                  value={terminals}
              >
                  <Column body={statusBody} header="Status" style={{width: '1%'}}></Column>
                  <Column body={detailsBody} header="Details" className="" style={{width: '15%'}}></Column>
                  <Column field="place_type" header="Place" sortable style={{width: '10%'}}></Column>
                  <Column body={infosBody} header="Infos" style={{width: '35%'}}></Column>
                  <Column body={manBody} header="Manage" style={{width: '2%'}}></Column>
              </DataTable>

          }

        </>
        )

        }


