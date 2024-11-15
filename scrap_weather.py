import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_weather_data():
    base_url = "https://www.timeanddate.com/weather/"
    countries = ["pakistan"]  # Add more countries as needed
    city_data = []

    for country in countries:
        url = f"{base_url}{country}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table containing the list of cities
        table = soup.find('table', class_='zebra fw tb-wt zebra va-m')

        if table:
            rows = table.find_all('tr')
            for row in rows[1:]:  # Skip the header row
                cols = row.find_all('td')
                if len(cols) >= 4:
                    city_name = cols[0].text.strip()
                    temperature = cols[3].text.strip()
                    city_data.append({
                        'City': city_name,
                        'Temperature (°C)': temperature
                    })

    # Convert the data into a DataFrame
    data = pd.DataFrame(city_data)
    return data


import streamlit as st

def main():
    st.title("Weather Forecast for Multiple Cities")

    # Scrape and display data
    st.header("Weather Data")
    weather_data = scrape_weather_data()

    # Search box for filtering cities
    city_search = st.text_input("Search for a city", "")
    if city_search:
        weather_data = weather_data[weather_data['City'].str.contains(city_search, case=False)]

    # Sorting options
    sort_by_temp = st.checkbox("Sort by Temperature", value=False)
    if sort_by_temp:
        weather_data['Temperature (°C)'] = weather_data['Temperature (°C)'].str.replace('°C', '').astype(float)
        weather_data = weather_data.sort_values(by='Temperature (°C)', ascending=False)

    st.dataframe(weather_data)

if __name__ == "__main__":
    main()
