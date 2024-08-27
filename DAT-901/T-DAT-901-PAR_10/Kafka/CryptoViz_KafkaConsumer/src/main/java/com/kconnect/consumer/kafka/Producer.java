package com.kconnect.consumer.kafka;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;
import org.springframework.kafka.support.SendResult;

import java.util.concurrent.CompletableFuture;

@Service
public class Producer {

    private static final Logger logger = LoggerFactory.getLogger(Producer.class);
    private static final String TOPIC = "articles";

    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;

    public void sendMessage(String key, String value) {
        CompletableFuture<SendResult<String, String>> future = kafkaTemplate.send(TOPIC, key, value);

        future.supplyAsync(() -> {
            // Perform some asynchronous computation
            // For example, fetching data from a database or making an HTTP call
            return 42;
        });

        // Add a callback to handle the result when it's available
        future.thenAccept(result -> {
            System.out.println("Result received: " + result);
            logger.info(String.format("Produced event to topic %s: key = %-10s value = %s", TOPIC, key, value));
            // Perform some action with the result
        });

        // Add error handling
        future.exceptionally(throwable -> {
            System.err.println("An error occurred: " + throwable.getMessage());
            // Handle the error
            return null; // or throw a RuntimeException
        });

        // Wait for the CompletableFuture to complete
        future.join(); // or use get() to block and get the result
    }

}