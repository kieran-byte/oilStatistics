# Oil Price and Production Correlation Analysis

This project aims to determine the potential correlation between oil prices and oil production over a specific period of time. The project involves obtaining historical data for oil prices and oil production for a given set of years and analyzing whether there's a correlation between these two factors.

## Overview

The project consists of the following main steps:

1. **Data Collection:**
   - [World oil production.](https://www.iea.org/data-and-statistics/charts/world-oil-production-by-region-1971-2020)
   - [World Oil Price.](https://github.com/datasets/oil-prices)

2. **Data Analysis:**
   - The obtained data is stored in csvs.
   - Data is then read in from csvs, new variables are created.
   - It is then stored in a sql file.
   - SQL data is read in and used to determine the correlation coefficient.

3. **Result Interpretation:**
   - The correlation coefficient between production and price is 0.31. 
   - This is lower than what I expected. However, this could be the case for a variety of reasons:
      - Supply is not perfectly elastic to demand, supply may only be correlated to the price of the previous year,
      - Supply can also change for geopolitical reasons e.g war, OPEC goals. More analysis would have to be done.

## Project Structure

The project directory includes the following components:

- `data/`: Directory containing the historical data files for oil prices and oil production.
-  root dir: Scripts or code files used to retrieve, process, and analyze the data.
- `README.md`: This file, providing an overview and instructions for the project.

## Usage

1. **Prerequisites:**
   - Python environment with necessary libraries (Pandas, NumPy, etc.) installed.

2. **Setup:**
   - Clone the repository to your local machine.

3. **Data Retrieval:**
   - Obtain historical data for oil prices and oil production for the desired period and save it in the `data/` directory.

4. **Data Analysis:**
   - Execute the analysis scripts to process and analyze the collected data.

5. **Result Interpretation:**
   - Review the generated results to understand the correlation analysis outcome.


## Image created in Power Apps using excel spreadsheet

![Oil Price vs Production](images/barChart.png)