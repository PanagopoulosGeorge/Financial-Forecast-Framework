# Financial Forecasting Data Management Framework

#### This project showcases an effort to design and develop a framework for managing and analyzing financial forecasting data. My endeavor to create a system for gathering, preserving, and organizing data associated with economic indicator forecasts requires segmentation into distinct components, each fulfilling a specific function.

> Specifically, the need to organize and compare financial forecast data from various sources, along with real indicator prices, highlights the importance for a programming tool that can interface with these sources and scrape the necessary data. Subsequently, this data must be extracted, transformed, and loaded into a database for subsequent analysis.



## Main Pillars of the System

The system architecture is divided into four main components:

### 1. Database Management Storage

The system will use **PostgreSQL** as the **database management system** (DBMS) to efficiently store financial forecast data. PostgreSQL is chosen for its robustness, scalability, and strong support for complex queries and transactions.

### 2. Web Scraping Environment

The web scraping environment will be implemented using **Requests** and if needed, **Scrapy**. These tools allow for effective extraction of financial forecast data from various online sources. **Requests** is suitable for straightforward HTTP requests which is most of the cases when dealing with financial data, while **Scrapy** offers a more advanced framework for large-scale, structured data scraping.

### 3. ETL /ELT Mechanism

The **ETL process** (Extract, Transform, Load) will be developed using **Python** and **SQL**  to standardize and process data from multiple sources. The extracted data will be loaded into the database in their original format. Additional views or mechanisms can be created to transform and standardize data.

### 4. User Interface and Visualization Tool (OPTIONAL)

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
