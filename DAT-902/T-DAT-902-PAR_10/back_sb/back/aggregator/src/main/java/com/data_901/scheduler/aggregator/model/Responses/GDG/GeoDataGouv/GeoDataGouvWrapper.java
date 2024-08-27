package com.data_901.scheduler.aggregator.model.Responses.GDG.GeoDataGouv;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import lombok.Data;

import java.util.ArrayList;

@Data
@JsonPropertyOrder({
        "total_count",
        "results"
})
@JsonIgnoreProperties(ignoreUnknown = true)
@Document(collection = "homepedia")
public class GeoDataGouvWrapper {
    @Id
    private int id;
    public int total_count;
    public ArrayList<GeoDataGouv> results;

    @JsonCreator
    public GeoDataGouvWrapper(@JsonProperty("total_count") int total_count, @JsonProperty("results") ArrayList<GeoDataGouv> results){
        this.total_count = total_count;
        this.results = results;
    }

    public void setId(int id){
        this.id = id;
    }
}
