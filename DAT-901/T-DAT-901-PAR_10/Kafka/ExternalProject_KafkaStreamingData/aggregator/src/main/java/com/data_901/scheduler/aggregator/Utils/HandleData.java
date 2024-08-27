package com.data_901.scheduler.aggregator.Utils;

import com.data_901.scheduler.aggregator.model.AggregateDays;
import com.data_901.scheduler.aggregator.model.AggregateHours;
import com.data_901.scheduler.aggregator.repository.AggregateDaysRepository;
import com.data_901.scheduler.aggregator.repository.AggregateHoursRepository;
import com.data_901.scheduler.aggregator.repository.LogRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class HandleData {

    private final AggregateDaysRepository rule_aggregate_days;
    private final AggregateHoursRepository rule_aggregate_hours;
    private final AggregateDays aggregate_days;
    private final AggregateHours aggregate_hours;
    private final LogRepository logRepository;

    HandleData(AggregateDays aggregate_days, AggregateHours aggregate_hours, LogRepository logRepository, AggregateDaysRepository rule_aggregate_days, AggregateHoursRepository rule_aggregate_hours){
        this.aggregate_days = aggregate_days;
        this.aggregate_hours = aggregate_hours;
        this.logRepository = logRepository;
        this.rule_aggregate_days = rule_aggregate_days;
        this.rule_aggregate_hours = rule_aggregate_hours;
    }
    public void rearrangeAll(){
        aggregate_hours.aggregate(logRepository, rule_aggregate_hours);
        aggregate_days.aggregate(rule_aggregate_days, rule_aggregate_hours);
    }
   public void maintain_3h(){
        aggregate_hours.aggregate(logRepository, rule_aggregate_hours);
    }
    public void maintain_48h(){
        aggregate_days.aggregate(rule_aggregate_days, rule_aggregate_hours);
    }
}
