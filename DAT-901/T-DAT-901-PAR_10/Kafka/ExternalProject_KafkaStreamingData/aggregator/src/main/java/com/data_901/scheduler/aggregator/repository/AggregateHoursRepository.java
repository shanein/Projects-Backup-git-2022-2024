package com.data_901.scheduler.aggregator.repository;

import com.data_901.scheduler.aggregator.model.AggregateHours;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface AggregateHoursRepository extends JpaRepository<AggregateHours, Long> {
}