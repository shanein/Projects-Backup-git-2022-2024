package com.data_901.scheduler.aggregator.repository;

import com.data_901.scheduler.aggregator.model.Logs.CryptoLog;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.*;

@Repository
public interface LogRepository extends JpaRepository<CryptoLog, Long> {
}