package com.kconnect.consumer;

import com.kconnect.consumer.kafka.Producer;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.WebApplicationType;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.kafka.config.KafkaListenerEndpointRegistry;
import org.springframework.kafka.listener.MessageListenerContainer;

import java.util.Objects;

@SpringBootApplication
public class SpringBootWithKafkaApplication{

	private final Producer producer;

	public static void main(String[] args) {
        SpringApplication application = new SpringApplication(SpringBootWithKafkaApplication.class);
        application.run(args);

	}

    @Bean
    public CommandLineRunner CommandLineRunnerBean() {
        return (args) -> {
                    MessageListenerContainer listenerContainer = kafkaListenerEndpointRegistry.getListenerContainer("myConsumer");
                    listenerContainer.start();
        };

	}
	@Autowired
    SpringBootWithKafkaApplication(Producer producer) {
        this.producer = producer;
    }
    @Autowired
    private KafkaListenerEndpointRegistry kafkaListenerEndpointRegistry;

}
