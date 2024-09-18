# Financial Forecasting Data Management Framework

#### This project showcases an effort to design and develop a framework for managing and analyzing financial forecasting data. My endeavor to create a system for gathering, preserving, and organizing data associated with economic indicator forecasts requires segmentation into distinct components, each fulfilling a specific function.

> Specifically, the need to organize and compare financial forecast data from various sources, along with real indicator prices, highlights the importance for a programming tool that can interface with these sources and scrape the necessary data. Subsequently, this data must be extracted, transformed, and loaded into a database for subsequent analysis.

## Main Pillars of the System Architecture

The system architecture is divided into four main components:

### 1. Database Management Storage

A **database management system** capable of storing efficiently the necessary data.

### 2. Web Scraping Environment

Communication with the various sources for the extraction of financial forecast data.

### 3. ETL Mechanism

**Extract, transform, and load** data from various sources into a standardized format, and finally load it into the database.

### 4. User Interface and/or Visualization Tool

End users will be able to interact with the data stored in the system through a **user interface** and/or a **visualization tool**.

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
