package com.data_901.server.server;

import com.data_901.server.server.Repository.LogRepository;
import com.data_901.server.server.model.CryptoLog;
import com.data_901.server.server.model.Data;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.KafkaConsumer;


import java.time.Duration;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.Properties;
import io.confluent.kafka.serializers.KafkaJsonDeserializerConfig;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.stereotype.Component;
import org.springframework.scheduling.annotation.Scheduled;

@Component
public class JsonConsumer {

    private Properties props = new Properties();
    private KafkaConsumer<String, Data> consumer;

    private LogRepository logRepository;
    @Autowired
    public JsonConsumer(LogRepository logRepository) {
        this.logRepository = logRepository;
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "pkc-60py3.europe-west9.gcp.confluent.cloud:9092");
        props.put("security.protocol", "SASL_SSL");
        props.put("sasl.jaas.config", "org.apache.kafka.common.security.plain.PlainLoginModule required username='"+Secrets.KAFKA_CLUSTER_KEY+"' password='"+Secrets.KAFKA_CLUSTER_SECRET+"';");
        props.put("sasl.mechanism", "PLAIN");
        props.put("client.dns.lookup", "use_all_dns_ips");
        props.put("session.timeout.ms", "45000");
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer");
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, "io.confluent.kafka.serializers.KafkaJsonDeserializer");
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "kafka_tutorial_example.jsonconsumer.v2");
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "latest");
        props.put(KafkaJsonDeserializerConfig.JSON_VALUE_TYPE, Data.class);
        consumer = new KafkaConsumer<String, Data>(props);
        consumer.subscribe(List.of("rides"));

    }
    public void consumeFromKafka() {
        System.out.println("Consuming form kafka started");
        var results = consumer.poll(Duration.of(1, ChronoUnit.SECONDS));
        var i = 0;
        do {
            for(ConsumerRecord<String, Data> result: results) {
                System.out.println("SYMBOLE --> " + result.value().s);
                logRepository.save(new CryptoLog(result.value().s, result.value().event_time, Double.parseDouble(result.value().k.c)));
            }
            results =  consumer.poll(Duration.of(1, ChronoUnit.SECONDS));
            System.out.println("RESULTS:::" + results.count());
            i++;
        }
        while(true);
    }

}
