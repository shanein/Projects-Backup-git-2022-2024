package com.kconnect.consumer.Controller;

import com.kconnect.consumer.kafka.Producer;
import com.kconnect.consumer.model.HtmlContent;
import com.kconnect.consumer.repository.HtmlContentRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;


@CrossOrigin(origins = "*")
@Controller
@RequestMapping("/kafka")
public class HtmlContentController {
    private final Producer producer;
    private final HtmlContentRepository htmlContentRepository;
    private final Logger logger = LoggerFactory.getLogger(HtmlContentController.class);
    @Autowired
    public HtmlContentController(Producer producer, HtmlContentRepository htmlContentRepository){
        this.producer = producer;
        this.htmlContentRepository = htmlContentRepository;
    }
    @PostMapping
    public ResponseEntity<?> send_to_kafka(@RequestBody HtmlContent request){
        producer.sendMessage("articles",request.content);
        return ResponseEntity.ok("Request processed successfully");

    }
    @GetMapping
    public ResponseEntity<?> handleGet(){
        return ResponseEntity.ok(htmlContentRepository.findAll());
    }
}
