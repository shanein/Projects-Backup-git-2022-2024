package com.data_901.server.server.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonIgnoreProperties
public class Data {
    private Long id;
    public String e;
    @JsonProperty("E")
    public long event_time;
    public String s;
    public K k;
}