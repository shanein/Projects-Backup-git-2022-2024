package com.data_901.scheduler.aggregator;

import com.data_901.scheduler.aggregator.Utils.HandleData;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.text.SimpleDateFormat;
import org.slf4j.Logger;
import java.util.Date;

@Component
public class ScheduledTasks {

    private static final Logger log = LoggerFactory.getLogger(ScheduledTasks.class);
    private HandleData handler;
    private static final SimpleDateFormat dateFormat = new SimpleDateFormat("HH:mm:ss");

    public ScheduledTasks(HandleData handler) {
        this.handler = handler;
    }
    @Scheduled(cron = "0 0 */4 * * *")
    public void maintain_3h() {
        log.info("The time is now {} main for 3h", dateFormat.format(new Date()));
        handler.maintain_3h();
    }
    @Scheduled(cron = "0 0 0 */2 * *")
    public void maintain_48h() {
        log.info("The time is now {} main for 48h", dateFormat.format(new Date()));
        handler.maintain_48h();
    }

}
