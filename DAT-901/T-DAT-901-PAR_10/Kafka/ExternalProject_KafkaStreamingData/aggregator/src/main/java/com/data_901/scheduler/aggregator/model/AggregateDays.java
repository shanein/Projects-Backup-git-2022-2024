package com.data_901.scheduler.aggregator.model;


import com.data_901.scheduler.aggregator.repository.AggregateDaysRepository;
import com.data_901.scheduler.aggregator.repository.AggregateHoursRepository;
import jakarta.persistence.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;


@Component
@Entity(name = "aggregate_days")
@Table(name = "aggregate_days")
public class AggregateDays extends Aggregate {
    @Transient
    private final Long INTERVAL_MILLS = 86400000L;
    @Transient
    private int iteration = 0;
    @Transient
    private Long previousValue = 0L;

    public AggregateDays() {
        super();
    }
    @Autowired
    public AggregateDays( Double max, Double min, Long interval_min, Long interval_max, Double median, Double medium, Integer count, String symbol) {
        super(max, min, interval_min, interval_max, median, medium, count, symbol);
    }


    public void aggregate(AggregateDaysRepository rule_aggregate_days, AggregateHoursRepository rule_aggregate_hours ) {
        List<AggregateDays> aggregate = new ArrayList<>();
        List<AggregateHours> all = rule_aggregate_hours.findAll();
        System.out.println(String.format(" TT-44=> %s", all.size()));
        List<AggregateHours> allSorted = all.stream().sorted(Aggregate.MIN_EVENT_TIME_COMPARATOR).toList();
        Map<String,List<Aggregate>> batch = allSorted.stream().collect(Collectors.groupingBy( aggregate_hour -> {
            if(aggregate_hour.getInterval_min() - this.previousValue > INTERVAL_MILLS){
                this.iteration++;
                this.previousValue = aggregate_hour.getInterval_min();
            }
            return String.format("BATCH_%d", iteration);
        }));


        batch.forEach((key, list) -> {
            Map<String, List<Aggregate>> groupBySymbol = allSorted.stream().collect(Collectors.groupingBy(aggregateHours -> aggregateHours.symbol));
            groupBySymbol.forEach((key_s, list_s) -> {
                Double max = list_s.stream().max(Aggregate.MEDIAN_PRICE_COMPARATOR).orElse(null).getMedian();
                Double min = list_s.stream().min(Aggregate.MEDIAN_PRICE_COMPARATOR).orElse(null).getMedian();
                Long interval_max = list_s.stream().max(Aggregate.MIN_EVENT_TIME_COMPARATOR).orElse(null).getInterval_max();
                Long interval_min = list_s.stream().min(Aggregate.MIN_EVENT_TIME_COMPARATOR).orElse(null).getInterval_min();
                int count = list_s.size();
                Double average = list_s.stream().map(Aggregate::getMedium).collect(Collectors.averagingDouble(Double::doubleValue));
                Double median = findMedian(list_s.stream().map(Aggregate::getMedian).sorted().toList());
                System.out.println("the Key  " + key_s);
                System.out.println("the List  "+ list_s);
                aggregate.add(new AggregateDays(max, min, interval_min, interval_max, median, average, count, key_s));
            });
        });
        rule_aggregate_days.saveAllAndFlush(aggregate);
        }
}
