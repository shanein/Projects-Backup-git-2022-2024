package com.data_901.scheduler.aggregator.Utils;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class MyConfiguration {

    @Bean
    public Double myDoubleBean() {
        return 0.0; // You can provide any initial value here
    }
    @Bean
    public Long myLongBean() {
        return 0L; // You can provide any initial value here
    }
    @Bean
    public Integer myIntegerBean() {
        return 0; // You can provide any initial value here
    }
    @Bean
    public String myStringBean() {
        return ""; // You can provide any initial value here
    }

}