import streamlit as st
import pandas as pd
import requests
from scholarly import scholarly
import time
from fuzzywuzzy import fuzz

# pathlib import
# import pathlib
# Define a dictionary to store translations for each language
translations = {
    'English': {
        'title': 'Publication Record Tool',
        'professor_name': 'Professor Name',
        'years': 'Years',
        'search': 'Search',
        'no_publications_found': 'No publications found.',
        'output_title': 'Title',
        'output_year': 'Year',
        'output_authors': 'Authors',
        'output_citations': 'Citations'
    },
    'Hindi': {
        'title': 'प्रकाशन रिकॉर्ड उपकरण',
        'professor_name': 'प्रोफेसर का नाम',
        'years': 'साल',
        'search': 'खोज',
        'no_publications_found': 'कोई प्रकाशन नहीं मिला.',
        'output_title': 'शीर्षक',
        'output_year': 'वर्ष',
        'output_authors': 'लेखक',
        'output_citations': 'उद्धरण'
    }
}

# Define a function to get the translations for the selected language
def get_translation(language, key):
    return translations[language].get(key, '')


def get_publications_from_google_scholar(professor_name, years):
    try:
        search_query = scholarly.search_author(professor_name)
        authors = list(search_query)  # iterate over the generator object and retrieve the results
        print("Google Scholar API response:", authors)
        publications = []
        for author in authors:
            if 'name' in author:
                similarity = fuzz.ratio(author['name'].lower(), professor_name.lower())
                if similarity > 80:  # if the similarity is greater than 80, we consider it a match
                    scholarly.fill(author)
                    pubs = author['publications']
                    for pub in pubs:
                        if 'year' in pub and str(pub['year']) in [str(year) for year in years]:
                            publications.append({
                                'title': pub['bib']['title'],
                                'year': pub['year'],
                                'authors': [author['name'] for author in pub['authors']],
                                'citations': pub['num_citations']
                            })
                    time.sleep(1)  # add a delay of 1 second between requests so that we don't get banned.
        return publications
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def get_publications_from_dblp(professor_name, years):
    url = f"https://dblp.org/search/publ/api?q={professor_name}&h=100&format=json"
    response = requests.get(url)
    data = response.json()
    publications = data['result']['hits']['hit']
    filtered_publications = []
    for pub in publications:
        if 'info' in pub and 'year' in pub['info'] and str(pub['info']['year']) in [str(year) for year in years]:
            filtered_publications.append({
                'title': pub['info']['title'],
                'year': pub['info']['year'],
                'authors': [author['text'] for author in pub['info']['authors']['author']],
                'citations': 0  # DBLP API does not provide citation count
            })
    return filtered_publications

def get_publications(professor_name, years):
    google_scholar_publications = get_publications_from_google_scholar(professor_name, years)
    dblp_publications = get_publications_from_dblp(professor_name, years)
    all_publications = google_scholar_publications + dblp_publications
    print("Publications:", all_publications)
    return all_publications
# Css test
# def load_css(file_path):
#     with open(file_path) as f:
#         st.html(f"<style>{f.read()}</style>")

# css_path=pathlib.Path("style.css")
# load_css(css_path)
# Css test ends

st.markdown("""
<style>
            stMain.st-emotion-cache-bm2z3a.ea3mdgi8{
            background-color:blue;
            }
            """,unsafe_allow_html=True)

language = st.selectbox('Language', ['English', 'Hindi'])

# Create the title
st.title(get_translation(language, 'title'))

professor_name = st.text_input(get_translation(language, 'professor_name'))
years = st.multiselect(get_translation(language, 'years'), range(1950, 2025))




if st.button('Search'):
# if st.button('Search',key="button"):
    print("Professor's name:", professor_name)
    print("Years:", years)
    publications = get_publications(professor_name, years)
    if publications:
        df = pd.DataFrame(publications)
        print("DataFrame:", df)
        df.to_excel('publishers.xlsx', index=False)  # write the data to an Excel file
        st.write(df)
        # st.write(df)
    else:
        st.write(get_translation(language, 'no_publications_found'))
