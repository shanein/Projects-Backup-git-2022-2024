package com.data_901.scheduler.aggregator.aggregator_dvf.dvf_transaction;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import lombok.Data;

import java.util.ArrayList;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
@JsonPropertyOrder({
        "nb_resultats",
        "resultats"
})
public class DVFTransactionWrapper {
    @JsonProperty("nb_resultats")
    public int nb_results;
    @JsonProperty("resultats")
    public ArrayList<DVFTransaction> results;

    @JsonCreator
    public DVFTransactionWrapper(@JsonProperty("nb_resultats") int nb_results, @JsonProperty("resultats") ArrayList<DVFTransaction> results){
        this.nb_results = nb_results;
        this.results = results;
    }

}
