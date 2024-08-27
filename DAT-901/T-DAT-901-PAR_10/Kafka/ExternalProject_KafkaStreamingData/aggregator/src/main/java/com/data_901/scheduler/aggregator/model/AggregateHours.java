package com.data_901.scheduler.aggregator.model;


import com.data_901.scheduler.aggregator.model.Logs.CryptoLog;
import com.data_901.scheduler.aggregator.repository.AggregateHoursRepository;
import com.data_901.scheduler.aggregator.repository.LogRepository;
import jakarta.persistence.Entity;
import jakarta.persistence.Transient;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;


@Component
@Entity(name = "aggregate_hours")
public  class AggregateHours extends Aggregate {
    @Transient
    private final Long INTERVAL_MILLS = 3600000L;
    @Transient
    private int iteration = 0;
    @Transient
    private Long previousValue = 0L;

    public AggregateHours() {
        super();
    }
    public AggregateHours(Double max, Double min, Long interval_min, Long interval_max, Double median, Double medium, Integer count, String symbol) {
        super(max, min, interval_min, interval_max, median, medium, count, symbol);
    }


    public void aggregate(LogRepository rule_logs, AggregateHoursRepository rule_aggregate_hours) {
        List<AggregateHours> aggregate = new ArrayList<>();
        List<CryptoLog> all = rule_logs.findAll();
        if(all.isEmpty()) return;

        List<CryptoLog> allSorted = all.stream().sorted(CryptoLog.EVENT_TIME_COMPARATOR).toList();
        Map<String,List<CryptoLog>> batch = allSorted.stream().collect(Collectors.groupingBy(cryptoLog -> {
            if(cryptoLog.event_time - this.previousValue > INTERVAL_MILLS){
                this.iteration++;
                this.previousValue = cryptoLog.event_time;
            }
            return String.format("BATCH_%d", iteration);
        }));

        batch.forEach((key, list) -> {
            Map<String,List<CryptoLog>> groupBySymbol = allSorted.stream().collect(Collectors.groupingBy(cryptoLog -> cryptoLog.symbol));

            groupBySymbol.forEach((key_s,list_s) -> {
                Double max = list_s.stream().max(CryptoLog.PRICE_COMPARATOR).orElse(null).price;
                Double min = list_s.stream().min(CryptoLog.PRICE_COMPARATOR).orElse(null).price;
                Long interval_max = list_s.stream().max(CryptoLog.EVENT_TIME_COMPARATOR).orElse(null).event_time;
                Long interval_min = list_s.stream().min(CryptoLog.EVENT_TIME_COMPARATOR).orElse(null).event_time;
                int count = list_s.size();
                Double average = list_s.stream().map(CryptoLog::getPrice).collect(Collectors.averagingDouble(Double::doubleValue));
                Double median = findMedian(list_s.stream().map(CryptoLog::getPrice).sorted().toList());
                System.out.println("All symbol :> " + key_s);

                aggregate.add(new AggregateHours(max, min, interval_min, interval_max, median, average, count, key_s));
            });
        });
        rule_aggregate_hours.saveAllAndFlush(aggregate);
        rule_logs.deleteAllByIdInBatch(all.stream().map(CryptoLog::getId).toList());
    }

}
