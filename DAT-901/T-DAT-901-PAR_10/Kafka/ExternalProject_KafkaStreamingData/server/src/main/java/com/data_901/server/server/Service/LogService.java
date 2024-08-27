
package com.data_901.server.server.Service;

import com.data_901.server.server.Repository.LogRepository;
import com.data_901.server.server.model.CryptoLog;
import jakarta.transaction.Transactional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;


@Service
@Transactional
@Slf4j
public class LogService{
    private final LogRepository repository;

    @Autowired
    public LogService(LogRepository repository) {
        this.repository = repository;
    }

    public void save_log(CryptoLog log) {
        System.out.println("saved log:: "+ log.symbol);
        repository.save(log);
    }
}
