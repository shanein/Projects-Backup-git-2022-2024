package com.data_901.server.server.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.transaction.Transactional;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.jpa.repository.Modifying;

import static jakarta.persistence.GenerationType.AUTO;


@Entity(name="cryptolog")
@Data
@NoArgsConstructor
@Transactional
public class CryptoLog {
    @Id
    @GeneratedValue(strategy = AUTO)
    @Column(name="ID")
    private Long id;
    public Long event_time;
    public String symbol;
    public Double price;

    public CryptoLog(String symbol, long event_time, Double price) {
        this.symbol = symbol;
        this.event_time = event_time;
        this.price = price;
    }
}
