package com.data_901.scheduler.aggregator.aggregator_dvf.PostgresRepository;

import com.data_901.scheduler.aggregator.model.Responses.DVFT.dvf_transaction.DVFTransaction;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface FinDataGouvRepository extends JpaRepository<DVFTransaction, Long> {
}

