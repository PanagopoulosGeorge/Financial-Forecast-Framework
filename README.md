# Financial Forecasting Data Management Framework

This project showcases an effort to design and develop a framework for managing and analyzing economic projections (such  as  GDP, headline inflation e.t.c) published by Financial institutions such as Banks and organizations like OECD and IMF. My endeavor to create a system for gathering and organizing data associated with economic indicator forecasts (and real measurements of the indicators) requires segmentation into distinct components, each fulfilling a specific function.

> Data from various sources (projections and real prices) will be extracted and loaded into a database for subsequent analysis.

## Installation

1. Install postgresql

   * **Install PostgreSQL:**
     - Download and install PostgreSQL from [here](https://www.postgresql.org/download/).
   * **Set Up the Database:**
     - Execute the scripts in the `install` folder in the following order to create the database, database user, database tables, and insert institutions, countries, and indicators.
2. Execute the scripts in install folder in order to create database, db user, db tables and insert institutions, countries and indicators.
3. Update `config.ini` within `conf` folder.
4. **Clone the repository | Create virtual environment:**

   ```sh
   git clone https://github.com/PanagopoulosGeorge/Financial-Forecast-Framework.git
   cd Financial-Forecast-Framework
   python -m venv venv
   venv\Scripts\activate.bat #source venv/bin/activate on Linux
   pip install -r requirements.txt
   ```

## Main Pillars of the System

The system architecture is divided into 3 main components:

### 1. Database Management Storage

The system will use **PostgreSQL** as the **database management system** (DBMS) to store financial forecast data. PostgreSQL is chosen for its robustness and scalability as well as Timescale, which is a version of Postgres focused on storing time series data.

### 2. Web Scraping - DB Loading Environment

The web scraping environment will be implemented using **Requests** and if needed, **Scrapy**. These tools allow for effective extraction of financial forecast data from various online sources. **Requests** is suitable for straightforward HTTP requests which is most of the cases when dealing with financial data, while **Scrapy** offers a more advanced framework for large-scale, structured data scraping.

The **ETL process** (Extract, Transform, Load) will be developed using **Python** and **SQL**  to standardize and process data from multiple sources. The extracted data will be loaded into the database in their original format. Additional views or mechanisms can be created to transform and standardize data.

### 3. User Interface and Visualization Tool (OPTIONAL)

A **Django web application** will serve as the user interface and visualization tool, allowing end users to interact with the stored data. Django is selected due to its ease of integration with databases, built-in admin capabilities, and scalability for web development, ensuring efficient management of the system.

## ER Diagram and Database Entities

Let's start by designing the **ER diagram** for the database. Based on the requirements you've outlined, we can identify three core entities:

### 1. Financial Institutions

These are the entities making predictions or reporting actual measurements for economic indicators.

### 2. Economic Indicators

These are the specific measurements or predictions (e.g., GDP, inflation rate, unemployment rate) made by the institutions. Each indicator will have data for a specific period, with values for both actuals and forecasts.

### 3. Geographical Area

These represent the regions for which the economic indicators are reported or predicted (e.g., countries, states, regions).

Based on the requirements here is a prototype of the ER diagram:

![1726680307518](images/README/1726680307518.png)

## Data Sources

### OECD (API documentation [here](https://gitlab.algobank.oecd.org/public-documentation/dotstat-migration/-/raw/main/OECD_Data_API_documentation.pdf))

The \*\*OECD\*\* provides a wealth of economic data used in this project for financial forecasting. Data such as GDP growth, inflation rates, and employment statistics will be obtained using the \*\*OECD Data API\*\*, which supports RESTful queries in formats like JSON, XML, and CSV.

### IMF (API documentation [here](https://www.imf.org/external/datamapper/api/help))

The \*\*International Monetary Fund (IMF)\*\* is another critical data provider. The IMF offers extensive economic data through its \*\*DataMapper API\*\*, enabling retrieval of time-series data related to global economic indicators.

## License

Copyright (c) [2024] [George Panagopoulos]

> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software.
