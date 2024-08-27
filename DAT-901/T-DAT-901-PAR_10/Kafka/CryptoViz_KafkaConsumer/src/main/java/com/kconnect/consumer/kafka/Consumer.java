package com.kconnect.consumer.kafka;

import com.kconnect.consumer.model.HtmlContent;
import com.kconnect.consumer.repository.HtmlContentRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;
import org.springframework.kafka.support.KafkaHeaders;
import org.springframework.messaging.handler.annotation.Header;

@Service
public class Consumer {
    private final HtmlContentRepository repo;
    private final Logger logger = LoggerFactory.getLogger(Consumer.class);

    @Autowired
    public Consumer(HtmlContentRepository repo) {
        this.repo = repo;
    }

    @KafkaListener(id = "myConsumer", topics = "articles", groupId = "spring-boot", autoStartup = "false")
    public void listen(String value,
        @Header(KafkaHeaders.RECEIVED_TOPIC) String topic) {
        logger.info(String.format("Consumed event from topic %s: key = %-10s value = %s", topic, "hello", value));
        HtmlContent html = new HtmlContent(value);
        repo.save(html);
    }
}