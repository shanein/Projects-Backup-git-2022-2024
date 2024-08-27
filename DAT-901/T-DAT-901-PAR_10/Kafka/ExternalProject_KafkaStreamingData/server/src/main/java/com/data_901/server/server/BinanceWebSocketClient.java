package com.data_901.server.server;

import com.data_901.server.server.model.Data;
import com.data_901.server.server.model.Log;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.java_websocket.WebSocket;
import org.java_websocket.client.WebSocketClient;
import org.java_websocket.exceptions.WebsocketNotConnectedException;
import org.java_websocket.framing.Framedata;
import org.java_websocket.framing.PingFrame;
import org.java_websocket.framing.PongFrame;
import org.java_websocket.handshake.ServerHandshake;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutionException;

public class BinanceWebSocketClient extends WebSocketClient {
    JsonProducer producer = new JsonProducer();

    public BinanceWebSocketClient(String url) throws URISyntaxException {
        super(new URI(url));
    }

    @Override
    public void onWebsocketPing(WebSocket conn, Framedata f) {
        super.onWebsocketPing(conn, f);
        System.out.println("I HAVE PING");
    }

    @Override
    public void onOpen(ServerHandshake handshakedata) {
        this.setConnectionLostTimeout(0);
        System.out.println("Connected to Binance WebSocket");
    }

    @Override
    public void onMessage(String message){
        List<Data> tosend = new ArrayList<>();

        System.out.println("Received message: " + message);
        try {
            Log log = new ObjectMapper().readValue(message, Log.class);
            tosend.add(log.data);
            producer.publishRides(tosend);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        } catch (ExecutionException e) {
            throw new RuntimeException(e);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public void onClose(int code, String reason, boolean remote) {
        System.out.println("Connection closed: " + reason);
    }

    @Override
    public void onError(Exception ex) {
        ex.printStackTrace();
    }

}
