package com.data_901.scheduler.aggregator;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
class AggregatorApplication {
	public static void main(String[] args) {SpringApplication.run(AggregatorApplication.class, args);}


}
