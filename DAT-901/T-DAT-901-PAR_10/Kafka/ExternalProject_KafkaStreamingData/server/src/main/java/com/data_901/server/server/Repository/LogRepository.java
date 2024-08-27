package com.data_901.server.server.Repository;

import com.data_901.server.server.model.CryptoLog;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.stereotype.Repository;

@Repository
public interface LogRepository extends JpaRepository<CryptoLog, Long> {
}