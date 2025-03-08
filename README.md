# Climate Analysis API

## Overview
This project provides a **Flask API** that serves climate analysis data from an SQLite database. The API is based on a prior analysis of historical weather data in Hawaii, focusing on **precipitation, temperature observations, and station metadata**.

## Project Files
- **`app.py`**: The Flask API that serves climate data.
- **`climate_starter.ipynb`**: A Jupyter Notebook that explores the dataset, conducts data analysis, and develops the necessary queries used in the Flask API. It includes:
  - Database connection and table reflection.
  - Data inspection and summary statistics.
  - Queries to extract precipitation, station, and temperature data.
  - Data visualization using Matplotlib.
- **`hawaii.sqlite`**: The SQLite database containing the climate data.
- **`hawaii_measurements.csv`**: Raw dataset containing precipitation and temperature readings.
- **`hawaii_stations.csv`**: Raw dataset containing station metadata.

## API Endpoints

### 1. Homepage (`/`)
Lists all available API routes.

### 2. Precipitation Data (`/api/v1.0/precipitation`)
- Converts the **last 12 months of precipitation data** into a dictionary `{date: precipitation}`.
- Returns the JSON representation of the dataset.

### 3. Stations (`/api/v1.0/stations`)
- Returns a **JSON list of stations** from the dataset.

### 4. Temperature Observations (`/api/v1.0/tobs`)
- Queries **temperature observations** for the most active station over the last 12 months.
- Returns a JSON list of `{date, temperature}`.

### 5. Temperature Summary (`/api/v1.0/<start>` & `/api/v1.0/<start>/<end>`)
- For a given **start date**, calculates **TMIN, TAVG, and TMAX** for all dates **greater than or equal** to the start.
- For a given **start and end date**, calculates **TMIN, TAVG, and TMAX** between those dates (inclusive).

## Running the API Locally

### **Step 1: Install Dependencies**
Ensure you have Python installed. Install the required dependencies with:
```sh
pip install flask sqlalchemy numpy pandas dateutil
```

### **Step 2: Run the Flask API**
Execute the following command in your terminal:
```sh
python app.py
```

### **Step 3: Access the API**
Once running, open a browser and navigate to:
- **Homepage:** [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
- **Precipitation:** [http://127.0.0.1:5000/api/v1.0/precipitation](http://127.0.0.1:5000/api/v1.0/precipitation)
- **Stations:** [http://127.0.0.1:5000/api/v1.0/stations](http://127.0.0.1:5000/api/v1.0/stations)
- **Temperature Observations:** [http://127.0.0.1:5000/api/v1.0/tobs](http://127.0.0.1:5000/api/v1.0/tobs)
- **Temperature Summary (Start Date):** [http://127.0.0.1:5000/api/v1.0/2017-01-01](http://127.0.0.1:5000/api/v1.0/2017-01-01)
- **Temperature Summary (Date Range):** [http://127.0.0.1:5000/api/v1.0/2017-01-01/2017-01-07](http://127.0.0.1:5000/api/v1.0/2017-01-01/2017-01-07)

## Notes
- Ensure the **database file (`hawaii.sqlite`) is in the correct path** (`Resources/hawaii.sqlite`).
- Modify the **SQLAlchemy engine path** in `app.py` if necessary.
- You can deploy this API to a cloud platform like **Render** for remote access.

## License
This project is open-source and available for modification and enhancement.
