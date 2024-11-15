import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

def scrape_news_data():
    url = "https://www.timeanddate.com/news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = []
    for item in soup.find_all('li', class_='tad-list-item'):
        # Extract title
        title_tag = item.find('h3', class_='tad-teaser__label')
        title = title_tag.text.strip() if title_tag else "No Title"

        # Extract summary
        summary_tag = item.find('div', class_='tad-teaser__abstract')
        summary = summary_tag.text.strip() if summary_tag else "No Summary"

        # Extract publication date
        date_tag = item.find('time')
        date = date_tag['datetime'] if date_tag else "No Date"

        # Extract link to full article
        link_tag = item.find('a', class_='tad-teaser__link')
        link = f"https://www.timeanddate.com{link_tag['href']}" if link_tag else "No Link"

        articles.append({
            'Title': title,
            'Summary': summary,
            'Date': date,
            'Link': link
        })

    # Convert to DataFrame
    return pd.DataFrame(articles)

### Step 3: Displaying Data in Streamlit
def main():
    st.title("Latest News from TimeAndDate.com")    
    # Scrape news data
    news_data = scrape_news_data()
    # Convert 'Date' to datetime format
    news_data['Date'] = pd.to_datetime(news_data['Date'], errors='coerce')    
    # Display data
    if not news_data.empty:
        #st.dataframe(news_data)
        for _, row in news_data.iterrows():
            st.markdown(f"### [{row['Title']}]({row['Link']})")            
            # Check if the 'Date' is a valid datetime object
            if pd.notnull(row['Date']):
                st.write(f"**Published on**: {row['Date'].strftime('%Y-%m-%d')}")
            else:
                st.write("**Published on**: Unknown Date")            
            st.write(f"**Summary**: {row['Summary']}")
            st.markdown("---")
    else:
        st.write("No articles found.")

if __name__ == "__main__":
    main()
