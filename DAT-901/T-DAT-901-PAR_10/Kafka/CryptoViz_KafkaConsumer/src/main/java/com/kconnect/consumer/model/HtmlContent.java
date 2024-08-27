package com.kconnect.consumer.model;


import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;

import static jakarta.persistence.GenerationType.AUTO;

@Data
@Entity
@NoArgsConstructor
@Table(name ="articles")
public class HtmlContent {
    @Id
    @GeneratedValue(strategy = AUTO)
    @Column(name="ID")
    private long id;
    @JsonProperty("html_content")
    @Column(columnDefinition = "TEXT")
    public String content;

    public HtmlContent(String content){
        this.content = content;
    }

}
