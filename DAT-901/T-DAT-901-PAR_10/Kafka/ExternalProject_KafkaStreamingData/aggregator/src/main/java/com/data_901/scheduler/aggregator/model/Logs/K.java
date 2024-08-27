package com.data_901.scheduler.aggregator.model.Logs;

import com.fasterxml.jackson.annotation.JsonProperty;

public class K{
    public Long Id;
    public long t;
    @JsonProperty("T")
    public long closeTime;
    public String s;
    public String i;
    public int f;
    @JsonProperty("L")
    public int last_trade_id;
    public String o;
    public String c;
    public String h;
    public String l;
    public String v;
    public int n;
    public boolean x;
    public String q;
    @JsonProperty("V")
    public String taker_base_asset_volume;
    @JsonProperty("Q")
    public String taker_buy_quote_asset_volume;
    @JsonProperty("B")
    public String b;
}
