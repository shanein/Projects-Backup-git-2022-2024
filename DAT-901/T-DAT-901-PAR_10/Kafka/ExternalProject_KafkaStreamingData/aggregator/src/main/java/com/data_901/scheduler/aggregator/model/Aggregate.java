package com.data_901.scheduler.aggregator.model;

import com.data_901.scheduler.aggregator.model.Logs.CryptoLog;
import com.data_901.scheduler.aggregator.repository.AggregateDaysRepository;
import com.data_901.scheduler.aggregator.repository.AggregateHoursRepository;
import com.data_901.scheduler.aggregator.repository.LogRepository;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Comparator;
import java.util.List;

import static jakarta.persistence.GenerationType.AUTO;


@Data
@MappedSuperclass
public abstract class Aggregate {
    @Id
    @GeneratedValue(strategy = AUTO)
    @Column(name="ID")
    private Long id;
    public String symbol;
    private Double max;
    private Double min;
    private Long interval_min;
    private Long interval_max;
    private Double median;
    private Double medium;
    private Integer count;
    @Transient
    public static final Comparator<Aggregate> MIN_EVENT_TIME_COMPARATOR = Comparator.comparingLong(Aggregate::getInterval_min);
    @Transient
    public static final Comparator<Aggregate> MEDIAN_PRICE_COMPARATOR = Comparator.comparingDouble(Aggregate::getMedian);
    public Aggregate(Double max, Double min, Long interval_min, Long interval_max, Double median, Double medium, Integer count, String symbol) {
        this.max = max;
        this.min = min;
        this.interval_min = interval_min;
        this.interval_max = interval_max;
        this.median = median;
        this.medium = medium;
        this.count = count;
        this.symbol = symbol;
    }
    public Aggregate(){

    }

    public Double findMedian(List<Double> list) {
        Double median;
        int size = list.size();
        if (size % 2 == 0) {
            int midIndex1 = size / 2 - 1;
            int midIndex2 = size / 2;
            median = (list.get(midIndex1) + list.get(midIndex2)) / 2.0;
        } else {
            int midIndex = size / 2;
            median = list.get(midIndex);
        }
        return median;
    }

    public Double getMax() {
        return max;
    }

    public void setMax(Double max) {
        this.max = max;
    }

    public Double getMin() {
        return min;
    }

    public void setMin(Double min) {
        this.min = min;
    }

    public Long getInterval_min() {
        return interval_min;
    }

    public void setInterval_min(Long interval_min) {
        this.interval_min = interval_min;
    }

    public Long getInterval_max() {
        return interval_max;
    }

    public void setInterval_max(Long interval_max) {
        this.interval_max = interval_max;
    }

    public Double getMedian() {
        return median;
    }

    public void setMedian(Double median) {
        this.median = median;
    }

    public Double getMedium() {
        return medium;
    }

    public void setMedium(Double medium) {
        this.medium = medium;
    }

}
