package com.data_901.scheduler.aggregator.model.Logs;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Comparator;

import static jakarta.persistence.GenerationType.AUTO;


@Entity(name="cryptolog")
@Data
@NoArgsConstructor
public class CryptoLog {
    @Id
    @GeneratedValue(strategy = AUTO)
    @Column(name="ID")
    private Long id;
    public Long event_time;
    public String symbol;
    public double price;
    public static final Comparator<CryptoLog> EVENT_TIME_COMPARATOR = Comparator.comparingLong(CryptoLog::getEvent_time);
    public static final Comparator<CryptoLog> PRICE_COMPARATOR = Comparator.comparingDouble(CryptoLog::getPrice);
    public Long getEvent_time() {
        return this.event_time;
    }
    public double getPrice() {
        return price;
    }
    public Long getId(){return id;}

    public CryptoLog(String symbol, long event_time, double price) {
        this.symbol = symbol;
        this.event_time = event_time;
        this.price = price;
    }
}
