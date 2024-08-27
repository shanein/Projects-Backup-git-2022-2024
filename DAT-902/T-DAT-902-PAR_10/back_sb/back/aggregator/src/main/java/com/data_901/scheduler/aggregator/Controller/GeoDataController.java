package com.data_901.scheduler.aggregator.Controller;


import com.data_901.scheduler.aggregator.Services.LandGeoDataRetrival;
import com.data_901.scheduler.aggregator.model.Responses.GDG.GeoDataGouv.GeoDataGouvWrapper;
import com.data_901.scheduler.aggregator.repository.MongoRepository.GeoDataGouvWRepository;
import lombok.extern.slf4j.Slf4j;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@CrossOrigin(origins = "*", allowedHeaders = "*")
@RestController
@Slf4j
@RequestMapping("/v1")
public class GeoDataController {
    private static final Logger logger = LoggerFactory.getLogger(GeoDataController.class);
    private LandGeoDataRetrival landGeoDataRetrival;
    private GeoDataGouvWRepository geoDataGouvWRepository;
    @Autowired
    public GeoDataController(LandGeoDataRetrival landGeoDataRetrival, GeoDataGouvWRepository geoDataGouvWRepository){
        this.landGeoDataRetrival = landGeoDataRetrival;
        this.  geoDataGouvWRepository = geoDataGouvWRepository;
    }

    @GetMapping("geoData")
    public ResponseEntity<?> getCommunesInDepartements(@RequestParam String likePostalCode){
        try{
            int postalCode = Integer.parseInt(likePostalCode.replace("*",""));
            Optional<GeoDataGouvWrapper> existingObject = geoDataGouvWRepository.findById(String.valueOf(postalCode));
            logger.info("here the cactus {}", existingObject);
            if(existingObject.isPresent()){
                logger.info("trying to save");
                return ResponseEntity.ok(existingObject);
            }else{
                GeoDataGouvWrapper tosave = landGeoDataRetrival.getGeoDataGouv(likePostalCode);
                tosave.setId(postalCode);
                geoDataGouvWRepository.save(tosave);
                return ResponseEntity.ok(tosave);
            }
        }catch (Exception e){
            logger.error("GeoDataGouvWrapper",e);
            return  new ResponseEntity<>(e, HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
}
