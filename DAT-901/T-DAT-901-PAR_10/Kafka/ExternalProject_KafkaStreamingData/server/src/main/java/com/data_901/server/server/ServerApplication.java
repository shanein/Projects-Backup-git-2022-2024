package com.data_901.server.server;

import com.data_901.server.server.Repository.LogRepository;
import com.data_901.server.server.Service.LogService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.scheduling.annotation.EnableScheduling;


@SpringBootApplication
@EnableScheduling
@ComponentScan({"com.data_901.server.server.Repository"})
public class ServerApplication {
    @Autowired

    public static void main(String[] args) {
		SpringApplication.run(ServerApplication.class, args);;

      /*  try {
            String binanceWebSocketUrl = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m";
            BinanceWebSocketClient client = new BinanceWebSocketClient(binanceWebSocketUrl);
            client.connect();
            JsonConsumer jsonConsumer = new JsonConsumer();
            jsonConsumer.consumeFromKafka();
            Thread.sleep(Long.MAX_VALUE);
        } catch (Exception e) {
            e.printStackTrace();
        }*/
	}
    @Bean
    CommandLineRunner commandLineRunner(LogRepository logRepository) {
    return  args -> {
        try {
            //String binanceWebSocketUrl = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m";
            String binanceWebSocketUrl = "wss://stream.binance.com:9443/stream?streams=ethusdt@kline_1m/dogeusdc@kline_1m/bnbusdt@kline_1m/trxusdt@kline_1m/ltcusdt@kline_1m/dotusdt@kline_1m/avaxusdt@kline_1m/maticusdt@kline_1m";
            BinanceWebSocketClient client = new BinanceWebSocketClient(binanceWebSocketUrl);
            client.connect();
            JsonConsumer jsonConsumer = new JsonConsumer(logRepository);
            jsonConsumer.consumeFromKafka();
            Thread.sleep(Long.MAX_VALUE);
        } catch (Exception e) {
            e.printStackTrace();
        }
    };

    };

}
	

