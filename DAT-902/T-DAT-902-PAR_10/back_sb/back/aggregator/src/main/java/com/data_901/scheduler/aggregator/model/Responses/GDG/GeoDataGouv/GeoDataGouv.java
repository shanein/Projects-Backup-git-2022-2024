
package com.data_901.scheduler.aggregator.model.Responses.GDG.GeoDataGouv;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({
    "insee_com",
    "postal_code",
    "nom_comm",
    "nom_dept",
    "nom_region",
    "statut",
    "z_moyen",
    "superficie",
    "population",
    "geo_point_2d",
    "geo_shape",
    "id_geofla",
    "code_comm",
    "code_cant",
    "code_arr",
    "code_dept",
    "code_reg"
})
public class GeoDataGouv {

    @JsonProperty("insee_com")
    private String inseeCom;
    @JsonProperty("postal_code")
    private String postalCode;
    @JsonProperty("nom_comm")
    private String nomComm;
    @JsonProperty("nom_dept")
    private List<String> nomDept;
    @JsonProperty("nom_region")
    private List<String> nomRegion;
    @JsonProperty("statut")
    private List<String> statut;
    @JsonProperty("z_moyen")
    private Double zMoyen;
    @JsonProperty("superficie")
    private Double superficie;
    @JsonProperty("population")
    private Double population;
    @JsonProperty("geo_point_2d")
    private GeoPoint2d geoPoint2d;
    @JsonProperty("geo_shape")
    private GeoShape geoShape;
    @JsonProperty("id_geofla")
    private String idGeofla;
    @JsonProperty("code_comm")
    private String codeComm;
    @JsonProperty("code_cant")
    private String codeCant;
    @JsonProperty("code_arr")
    private String codeArr;
    @JsonProperty("code_dept")
    private String codeDept;
    @JsonProperty("code_reg")
    private String codeReg;
    @JsonIgnore
    private Map<String, Object> additionalProperties = new LinkedHashMap<String, Object>();

    @JsonProperty("insee_com")
    public String getInseeCom() {
        return inseeCom;
    }

    @JsonProperty("insee_com")
    public void setInseeCom(String inseeCom) {
        this.inseeCom = inseeCom;
    }

    @JsonProperty("postal_code")
    public String getPostalCode() {
        return postalCode;
    }

    @JsonProperty("postal_code")
    public void setPostalCode(String postalCode) {
        this.postalCode = postalCode;
    }

    @JsonProperty("nom_comm")
    public String getNomComm() {
        return nomComm;
    }

    @JsonProperty("nom_comm")
    public void setNomComm(String nomComm) {
        this.nomComm = nomComm;
    }

    @JsonProperty("nom_dept")
    public List<String> getNomDept() {
        return nomDept;
    }

    @JsonProperty("nom_dept")
    public void setNomDept(List<String> nomDept) {
        this.nomDept = nomDept;
    }

    @JsonProperty("nom_region")
    public List<String> getNomRegion() {
        return nomRegion;
    }

    @JsonProperty("nom_region")
    public void setNomRegion(List<String> nomRegion) {
        this.nomRegion = nomRegion;
    }

    @JsonProperty("statut")
    public List<String> getStatut() {
        return statut;
    }

    @JsonProperty("statut")
    public void setStatut(List<String> statut) {
        this.statut = statut;
    }

    @JsonProperty("z_moyen")
    public Double getzMoyen() {
        return zMoyen;
    }

    @JsonProperty("z_moyen")
    public void setzMoyen(Double zMoyen) {
        this.zMoyen = zMoyen;
    }

    @JsonProperty("superficie")
    public Double getSuperficie() {
        return superficie;
    }

    @JsonProperty("superficie")
    public void setSuperficie(Double superficie) {
        this.superficie = superficie;
    }

    @JsonProperty("population")
    public Double getPopulation() {
        return population;
    }

    @JsonProperty("population")
    public void setPopulation(Double population) {
        this.population = population;
    }

    @JsonProperty("geo_point_2d")
    public GeoPoint2d getGeoPoint2d() {
        return geoPoint2d;
    }

    @JsonProperty("geo_point_2d")
    public void setGeoPoint2d(GeoPoint2d geoPoint2d) {
        this.geoPoint2d = geoPoint2d;
    }

    @JsonProperty("geo_shape")
    public GeoShape getGeoShape() {
        return geoShape;
    }

    @JsonProperty("geo_shape")
    public void setGeoShape(GeoShape geoShape) {
        this.geoShape = geoShape;
    }

    @JsonProperty("id_geofla")
    public String getIdGeofla() {
        return idGeofla;
    }

    @JsonProperty("id_geofla")
    public void setIdGeofla(String idGeofla) {
        this.idGeofla = idGeofla;
    }

    @JsonProperty("code_comm")
    public String getCodeComm() {
        return codeComm;
    }

    @JsonProperty("code_comm")
    public void setCodeComm(String codeComm) {
        this.codeComm = codeComm;
    }

    @JsonProperty("code_cant")
    public String getCodeCant() {
        return codeCant;
    }

    @JsonProperty("code_cant")
    public void setCodeCant(String codeCant) {
        this.codeCant = codeCant;
    }

    @JsonProperty("code_arr")
    public String getCodeArr() {
        return codeArr;
    }

    @JsonProperty("code_arr")
    public void setCodeArr(String codeArr) {
        this.codeArr = codeArr;
    }

    @JsonProperty("code_dept")
    public String getCodeDept() {
        return codeDept;
    }

    @JsonProperty("code_dept")
    public void setCodeDept(String codeDept) {
        this.codeDept = codeDept;
    }

    @JsonProperty("code_reg")
    public String getCodeReg() {
        return codeReg;
    }

    @JsonProperty("code_reg")
    public void setCodeReg(String codeReg) {
        this.codeReg = codeReg;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperty(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

}
