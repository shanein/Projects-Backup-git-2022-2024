# Crypto VIZ

## Introduction

Crypto VIZ is a web application designed to provide real-time analysis and data visualization on cryptocurrencies.

## Architecture

The application consists of five main components:

- **Online Web Scraper**: Utilizes Selenium to fetch data from CoinJournal.
- **Producer/Consumer Kafka**: Manages real-time data flows between the scraper and data processing.
- **Backend**: Django backend with rest_framework for API creation, account, and features.
- **Frontend**: User interface built with Vue.js.
- **Database**: PostgreSQL

## Interactions

- Data is initially collected via Selenium and sent to Kafka for real-time processing.
- Django serves as an API, enabling Vue.js to access various functionalities.
- Vue.js displays both scraped data and CoinGecko data visualized with amCharts 5.

## Technical Choices

- **Frontend**: Vue.js for its reactivity and ease of integration.
- **Backend**: Django for a robust and scalable platform.
- **Data Flow Management**: Apache Kafka for reliable real-time data processing.
- **Data Visualization**: amCharts 5 for interactive and dynamic charts.
- **Scraping**: Selenium for automated web page interactions.
- **API Integration**: CoinGecko API for comprehensive real-time cryptocurrency data.

## Backend Features

- **For Any User**: Fetch specific or all cryptocurrencies, with real-time data from an external API or local history if the API is unavailable.
- **For Registered Users**: Subscribe to, unsubscribe from, and list subscriptions to specific cryptocurrencies.
- **For Admins**: Create and delete cryptocurrencies in the database, ensuring data accuracy through external API updates.

## Authentication and User Management

- Secure sign-up and login processes with BCrypt for password hashing.
- Users can update personal information and passwords, or delete their accounts, ensuring data privacy.

## Frontend Visualization and Features

- **News Crypto from Scraping**: Directly consumed by Vue.js from Kafka.
- **Cryptos and Market Cap Treemap**: Main page features a list of cryptocurrencies and a treemap visualizing market capitalization.
- **Candlestick Charts and Comparisons**: Specific crypto pages offer candlestick charts for price evolution and comparative graphs against Bitcoin.

## Conclusion

Crypto VIZ leverages advanced technologies for a robust and intuitive platform dedicated to cryptocurrency data analysis and visualization.
