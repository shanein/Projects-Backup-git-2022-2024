package com.data_901.scheduler.aggregator.repository.MongoRepository;

import org.springframework.data.mongodb.repository.MongoRepository;

public interface GeoDataGouvWRepository extends MongoRepository<com.data_901.scheduler.aggregator.model.Responses.GDG.GeoDataGouv.GeoDataGouvWrapper, String> {
}
