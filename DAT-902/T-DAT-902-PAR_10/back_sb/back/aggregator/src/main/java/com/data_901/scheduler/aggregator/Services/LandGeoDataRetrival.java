package com.data_901.scheduler.aggregator.Services;

import com.data_901.scheduler.aggregator.model.Responses.GDG.GeoDataGouv.GeoDataGouvWrapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class LandGeoDataRetrival {

    private static final Logger logger = LoggerFactory.getLogger(LandGeoDataRetrival.class);
    private final RestTemplate restTemplate;
    private int REQUEST_PAGE_SIZE = 100;
    private String BASE_URL = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/correspondance-code-insee-code-postal/records";

    @Autowired
    public LandGeoDataRetrival(RestTemplateBuilder restTemplateBuilder) {
        this.restTemplate = restTemplateBuilder.build();
    }

    public GeoDataGouvWrapper getGeoDataGouv(String postalCode) {
        int neededIteration = 1;
        Boolean isFinish = false;
        GeoDataGouvWrapper temporaryValues = null;
        int offset = 0; // Example offset
        do{
            if(offset == 0){
                temporaryValues = restTemplate.getForObject(getParameterizedUrl(postalCode, offset*REQUEST_PAGE_SIZE), GeoDataGouvWrapper.class);
                neededIteration = (int) Math.ceil(temporaryValues.total_count/REQUEST_PAGE_SIZE);
            }else{
                GeoDataGouvWrapper freshData = restTemplate.getForObject(getParameterizedUrl(postalCode, offset*REQUEST_PAGE_SIZE), GeoDataGouvWrapper.class);
                temporaryValues.results.addAll(freshData.results);
            }
            isFinish = offset == neededIteration;
            offset++;
            logger.info("the actual count: {}\n should be reached: {}", temporaryValues.results.size(), temporaryValues.total_count);
        }while(!isFinish);

        return temporaryValues;
    }
    private String getParameterizedUrl(String likePostalCode, int offset){
        return BASE_URL + "?offset="+ offset+"&limit=100&where=postal_code LIKE '"+likePostalCode+"'";
    }
}
