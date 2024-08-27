
package com.data_901.scheduler.aggregator.aggregator_dvf.dvf_transaction;

import com.fasterxml.jackson.annotation.*;
import jakarta.persistence.*;
import lombok.Data;

@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonIgnoreProperties(ignoreUnknown = true)
@JsonPropertyOrder({
    "date_mutation",
    "nature_mutation",
    "valeur_fonciere",
    "numero_voie",
    "suffixe_numero",
    "type_voie",
    "code_voie",
    "voie",
    "code_postal",
    "commune",
    "code_departement",
    "code_commune",
    "numero_volume",
    "nombre_lots",
    "code_type_local",
    "type_local",
    "identifiant_local",
    "surface_relle_bati",
    "nombre_pieces_principales",
    "surface_terrain",
    "lat",
    "lon",
})
@Entity
@Table(name = "real_estate_transaction", indexes = {
        @Index(name = "idx_code_postal", columnList = "codePostal")
})
public class DVFTransaction {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @JsonIgnore
    private String numeroDisposition;
    @JsonProperty("date_mutation")
    private String dateMutation;
    @JsonProperty("nature_mutation")
    private String natureMutation;
    @JsonProperty("valeur_fonciere")
    private Integer valeurFonciere;
    @JsonProperty("numero_voie")
    private String numeroVoie;
    @JsonProperty("suffixe_numero")
    private String suffixeNumero;
    @JsonProperty("type_voie")
    private String typeVoie;
    @JsonProperty("code_voie")
    private String codeVoie;
    @JsonProperty("voie")
    private String voie;
    @JsonProperty("code_postal")
    private String codePostal;
    @JsonProperty("commune")
    private String commune;
    @JsonProperty("code_departement")
    private String codeDepartement;
    @JsonProperty("code_commune")
    private String codeCommune;
    @JsonProperty("nombre_lots")
    private String nombreLots;
    @JsonProperty("code_type_local")
    private String codeTypeLocal;
    @JsonProperty("type_local")
    private String typeLocal;
    @JsonProperty("surface_relle_bati")
    private Integer surfaceRelleBati;
    @JsonProperty("nombre_pieces_principales")
    private Integer nombrePiecesPrincipales;
    @JsonProperty("surface_terrain")
    private String surfaceTerrain;
    @JsonProperty("lat")
    private Double lat;
    @JsonProperty("lon")
    private Double lon;

}
