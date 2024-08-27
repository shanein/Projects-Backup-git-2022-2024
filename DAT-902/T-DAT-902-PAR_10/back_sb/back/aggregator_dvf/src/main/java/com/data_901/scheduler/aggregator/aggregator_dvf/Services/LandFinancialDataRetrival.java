package com.data_901.scheduler.aggregator.aggregator_dvf.Services;

import com.data_901.scheduler.aggregator.model.Responses.DVFT.dvf_transaction.DVFTransactionWrapper;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;


@Service
public class LandFinancialDataRetrival {
    private static final Logger logger = LoggerFactory.getLogger(LandFinancialDataRetrival.class);
    private final RestTemplate restTemplate;
    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    public LandFinancialDataRetrival(RestTemplateBuilder restTemplateBuilder, ObjectMapper objectMapper) {
        this.restTemplate = restTemplateBuilder.build();
        this.objectMapper = objectMapper;
    }
    public DVFTransactionWrapper getFinancialDataGouv(String url) {

        DVFTransactionWrapper dvfTransactionWrapper = null;

        try {
            HttpHeaders headers = new HttpHeaders();
            headers.set("User-Agent", "Wget/1.21.1");
            HttpEntity<String> entity = new HttpEntity<>(headers);
            ResponseEntity<String> response = restTemplate.exchange(url, HttpMethod.GET, entity, String.class);

            if (response.getStatusCode().is2xxSuccessful()) {
                String responseBody = response.getBody();
                logger.info("Response body: {}", responseBody);
                return objectMapper.readValue(responseBody, DVFTransactionWrapper.class);

            } else if (response.getStatusCode().is3xxRedirection()) {
                String newUrl = response.getHeaders().getLocation().toString();
                logger.info("Redirecting to URL: {}", newUrl);
                return getFinancialDataGouv(newUrl); // Recursive call to handle redirection

            } else {
                logger.error("Unexpected status code: {}", response.getStatusCode());
                logger.error("Response body: {}", response.getBody());
                throw new RuntimeException("Unexpected status code: " + response.getStatusCode());
            }
        }catch (JsonProcessingException e){
            logger.error("something wrong here {}", e);
        }
        return dvfTransactionWrapper;
    }


}
