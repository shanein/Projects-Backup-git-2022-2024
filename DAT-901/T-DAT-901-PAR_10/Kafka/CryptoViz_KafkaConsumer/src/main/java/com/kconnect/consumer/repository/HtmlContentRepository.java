package com.kconnect.consumer.repository;

import com.kconnect.consumer.model.HtmlContent;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface HtmlContentRepository extends JpaRepository<HtmlContent, Long> {
}
