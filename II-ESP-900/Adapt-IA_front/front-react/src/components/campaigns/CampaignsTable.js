import React, { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import { classNames } from "primereact/utils";
import { FilterMatchMode, FilterOperator } from "primereact/api";
import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";
import { InputText } from "primereact/inputtext";
import { Dropdown } from "primereact/dropdown";
import { MultiSelect } from "primereact/multiselect";
import { Tag } from "primereact/tag";
import { TriStateCheckbox } from "primereact/tristatecheckbox";
import "../../styles/Campaigns.scss";
import { useNavigate } from "react-router-dom";

function CampaignsTable({ setAdSelected, setView }) {
  const campaigns = useSelector((state) => state.ads.ads);
  const navigate = useNavigate();
  const [customers, setCustomers] = useState(null);
  const [filters, setFilters] = useState({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS },
    name: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
    is_smart: { value: null, matchMode: FilterMatchMode.EQUALS },
    is_valid: { value: null, matchMode: FilterMatchMode.EQUALS },
    is_active: { value: null, matchMode: FilterMatchMode.EQUALS },
    start_date: { value: null, matchMode: FilterMatchMode.CONTAINS },
    end_date: { value: null, matchMode: FilterMatchMode.CONTAINS },
  });
  const [loading, setLoading] = useState(true);
  const [globalFilterValue, setGlobalFilterValue] = useState("");
  const [representatives] = useState([
    { name: "Amy Elsner", image: "amyelsner.png" },
    { name: "Anna Fali", image: "annafali.png" },
    { name: "Asiya Javayant", image: "asiyajavayant.png" },
    { name: "Bernardo Dominic", image: "bernardodominic.png" },
    { name: "Elwin Sharvill", image: "elwinsharvill.png" },
    { name: "Ioni Bowcher", image: "ionibowcher.png" },
    { name: "Ivan Magalhaes", image: "ivanmagalhaes.png" },
    { name: "Onyama Limba", image: "onyamalimba.png" },
    { name: "Stephen Shaw", image: "stephenshaw.png" },
    { name: "XuXue Feng", image: "xuxuefeng.png" },
  ]);
  const [statuses] = useState(["IA", "Classique"]);

  const getSeveritySmart = (smart) => {
    if (smart) {
      return "success";
    } else {
      return "info";
    }
  };

  const getSeverityActive = (active) => {
    if (active) {
      return "success";
    } else {
      return "warning";
    }
  };

  useEffect(() => {
    if (campaigns) {
      setCustomers(campaigns);
      setLoading(false);
    }
  }, []);

  const getDates = (data) => {
    return [...(data || [])].map((d) => {
      console.log("d : ", d);
      d.start_date = new Date(d.start_date);
      d.end_date = new Date(d.end_date);

      return d;
    });
  };

  const getCustomers = (data) => {
    return [...(data || [])].map((d) => {
      d.date = new Date(d.date);

      return d;
    });
  };

  const onGlobalFilterChange = (e) => {
    const value = e.target.value;
    let _filters = { ...filters };

    _filters["global"].value = value;

    setFilters(_filters);
    setGlobalFilterValue(value);
  };

  const renderHeader = () => {
    return (
      <div className="flex justify-content-end">
        <span className="p-input-icon-left">
          <i className="pi pi-search" />
          <InputText
            value={globalFilterValue}
            onChange={onGlobalFilterChange}
            placeholder="Keyword Search"
          />
        </span>
      </div>
    );
  };

  const isSmartBodyTemplate = (rowData) => {
    return (
      <div className="flex align-items-center gap-2">
        <Tag
          value={rowData.is_smart ? "IA" : "Classique"}
          severity={getSeveritySmart(rowData.is_smart)}
        />
      </div>
    );
  };
  const startDateBodyTemplate = (rowData) => {
    let date = new Date(rowData.start_date);
    let hours = date.getHours() + ":" + date.getMinutes();
    date = date.toLocaleDateString();

    return (
      <div className="flex align-items-center gap-2">
        <span>
          {date} {hours}
        </span>
      </div>
    );
  };

  const endDateBodyTemplate = (rowData) => {
    let date = new Date(rowData.end_date);
    let hours = date.getHours() + ":" + date.getMinutes();
    date = date.toLocaleDateString();

    return (
      <div className="flex align-items-center gap-2">
        <span>
          {date} {hours}
        </span>
      </div>
    );
  };

  // const representativeBodyTemplate = (rowData) => {
  //   const representative = rowData.representative;

  //   return (
  //     <div className="flex align-items-center gap-2">
  //       <img
  //         //   alt={representative.name}
  //         src={`https://primefaces.org/cdn/primereact/images/avatar/${representative.image}`}
  //         width="32"
  //       />
  //     </div>
  //   );
  // };

  // const representativesItemTemplate = (option) => {
  //   return (
  //     <div className="flex align-items-center gap-2">
  //       <img
  //         alt={option.name}
  //         src={`https://primefaces.org/cdn/primereact/images/avatar/${option.image}`}
  //         width="32"
  //       />
  //       <span>{option.name}</span>
  //     </div>
  //   );
  // };

  const isActiveBodyTemplate = (rowData) => {
    return (
      <Tag
        value={rowData.is_active ? "Active" : "Inactive"}
        severity={getSeverityActive(rowData.is_active)}
      />
    );
  };

  const statusItemTemplate = (option) => {
    return (
      <Tag
        value={option}
        severity={getSeveritySmart(option === "IA" ? true : false)}
      />
    );
  };

  //   const verifiedBodyTemplate = (rowData) => {
  //     return (
  //       <i
  //         className={classNames("pi", {
  //           "true-icon pi-check-circle": rowData.is_active,
  //           "false-icon pi-times-circle": !rowData.is_active,
  //         })}
  //       ></i>
  //     );
  //   };
  const isActiveBodyTemplate2 = (rowData) => {
    return (
      <i
        className={classNames("pi", {
          "text-green-500 pi-check-circle": rowData.is_active,
          "text-red-500 pi-times-circle": !rowData.is_active,
        })}
      ></i>
    );
  };

  const isValidBodyTemplate = (rowData) => {
    return (
      <i
        className={classNames("pi", {
          "text-green-500 pi-check-circle": rowData.is_valid,
          "text-red-500 pi-times-circle": !rowData.is_valid,
        })}
      ></i>
    );
  };

  // const representativeRowFilterTemplate = (options) => {
  //   return (
  //     <MultiSelect
  //       value={options.value}
  //       options={representatives}
  //       itemTemplate={representativesItemTemplate}
  //       onChange={(e) => options.filterApplyCallback(e.value)}
  //       optionLabel="name"
  //       placeholder="Any"
  //       className="p-column-filter"
  //       maxSelectedLabels={1}
  //       style={{ minWidth: "14rem" }}
  //     />
  //   );
  // };

  //   const isActiveRowFilterTemplate = (options) => {
  // console.log("Options : ", options);

  // return (
  //   <Dropdown
  //     value={options.value}
  //     options={statuses}
  //     // onChange={(e) => {
  //     //   console.log("e : ", e);
  //     //   e.value == "IA"
  //     //     ? options.filterApplyCallback(true)
  //     //     : options.filterApplyCallback(false);
  //     // }}
  //     onChange={(e) => {
  //       console.log("e.value : ", e.value);
  //       const filterValue = e.value === "IA"; // e.value est soit "IA" soit "Classique"
  //       console.log("filterValue : ", filterValue);
  //       options.filterApplyCallback(filterValue); // Appliquer le filtre avec la valeur booléenne
  //     }}
  //     itemTemplate={statusItemTemplate}
  //     placeholder="Select One"
  //     className="p-column-filter"
  //     showClear
  //     style={{ minWidth: "12rem" }}
  //   />
  // );
  // };
  const isActiveRowFilterTemplate = (options) => {
    const handleChange = (e) => {
      const filterValue = e.value === "IA";
      if (options && options.filterApplyCallback) {
        options.filterApplyCallback(filterValue);
      }
    };

    return (
      <Dropdown
        value={options}
        options={statuses}
        onChange={handleChange}
        itemTemplate={statusItemTemplate}
        placeholder="Select One"
        className="p-column-filter"
        showClear
        style={{ minWidth: "12rem" }}
        size={"small"}
      />
    );
  };

  const isSmartRowFilterTemplate = (options) => {
    const handleChange = (e) => {
      const filterValue = e.value === "IA";
      if (options && options.filterApplyCallback) {
        options.filterApplyCallback(filterValue);
      }
    };

    return (
      <Dropdown
        value={options.value}
        options={statuses}
        optionLabel="name"
        onChange={handleChange}
        itemTemplate={statusItemTemplate}
        placeholder="Select One"
        className="p-column-filter"
        // showClear
        style={{ minWidth: "12rem" }}
      />
    );
  };

  const isActiveRowFilterTemplate2 = (options) => {
    return (
      <TriStateCheckbox
        value={options.value}
        onChange={(e) => options.filterApplyCallback(e.value)}
      />
    );
  };

  const onRowSelect = (event) => {
    setAdSelected(event.data);
    // setView("ad");
    navigate(`/campaign/${event.data.id}`);
  };

  const header = renderHeader();

  useEffect(() => {
    if (campaigns) {
      setCustomers(campaigns);
    }
  }, [campaigns]);

  return (
    <div className="card" style={{ margin: "auto" }}>
      <DataTable
        value={customers}
        paginator
        rows={10}
        dataKey="id"
        filters={filters}
        filterDisplay="row"
        loading={loading}
        globalFilterFields={[
          "name",
          "is_smart",
          "is_active",
          "status",
          "description",
          "start_date",
          "end_date",
        ]}
        header={header}
        emptyMessage="No campaigns found."
        selectionMode="single"
        onRowSelect={onRowSelect}
        id="campaigns-table"
        size="small"
        scrollable
        scrollHeight="calc(100vh - 350px)"
        lazy
      >
        <Column
          field="is_active"
          header="Is Active"
          style={{ minWidth: "6rem" }}
          body={isActiveBodyTemplate2}
          filter
          showFilterMenu={false}
          filterElement={isActiveRowFilterTemplate2}
        />
        <Column
          field="is_valid"
          header="Is Valid"
          style={{ minWidth: "6rem" }}
          body={isValidBodyTemplate}
          filter
          showFilterMenu={false}
          filterElement={isActiveRowFilterTemplate2}
        />
        {/* <Column
          field="is_active"
          header="Is Active"
          showFilterMenu={false}
          filterMenuStyle={{ width: "14rem" }}
          style={{ minWidth: "12rem" }}
          body={isActiveBodyTemplate}
          dataType="boolean"
          filter
          filterElement={isActiveRowFilterTemplate}
        /> */}
        <Column
          field="name"
          header="Name"
          filter
          filterPlaceholder="Search by name"
          style={{ minWidth: "12rem" }}
        />
        <Column
          header="Campaign Type"
          filterField="is_smart"
          style={{ minWidth: "12rem" }}
          body={isSmartBodyTemplate}
          showFilterMenu={false}
          filter
          //   filterPlaceholder="Search by country"
          filterElement={isSmartRowFilterTemplate}
        />
        <Column
          header="Video Preview"
          body={(rowData) =>
            rowData.video_url ? (
              <img
                src={rowData.video_url
                  .replace("mp4", "jpg")
                  .replace("mov", "jpg")}
                alt="Video Thumbnail"
                style={{ cursor: "pointer", width: "60px", height: "auto" }}
              />
            ) : rowData.videoUrl ? (
              <img
                src={rowData.videoUrl.replace(/\.mp4|\.mov/gi, ".jpg")}
                alt="Miniature de la vidéo"
                style={{ cursor: "pointer", width: "60px", height: "auto" }}
              />
            ) : (
              <></>
            )
          }
          style={{ minWidth: "8rem" }}
        />
        <Column
          header="Date From"
          filterField="start_date"
          style={{ minWidth: "12rem" }}
          body={startDateBodyTemplate}
          filter
          filterPlaceholder="Search by country"
        />
        <Column
          header="Date To"
          filterField="end_date"
          style={{ minWidth: "12rem" }}
          body={endDateBodyTemplate}
          filter
          filterPlaceholder="Search by country"
        />

        {/* <Column
          header="Agent"
          filterField="representative"
          showFilterMenu={false}
          filterMenuStyle={{ width: "14rem" }}
          style={{ minWidth: "14rem" }}
          body={representativeBodyTemplate}
          filter
          filterElement={representativeRowFilterTemplate}
        /> */}
      </DataTable>
    </div>
  );
}

export default CampaignsTable;
