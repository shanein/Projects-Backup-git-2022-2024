package com.data_901.scheduler.aggregator.Utils;

import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.stereotype.Component;

@Component
public class MyApplicationRunner implements ApplicationRunner {

    private final HandleData handler;

    public MyApplicationRunner(HandleData handler) {
        this.handler = handler;
    }

    @Override
    public void run(ApplicationArguments args) throws Exception {
        handler.rearrangeAll();
    }
}
