import streamlit as st
import pandas as pd
import requests
from scholarly import scholarly
import time
from fuzzywuzzy import fuzz

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
                    time.sleep(1)  # add a delay of 1 second between requests
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

st.title('Publication Record Tool')

professor_name = st.text_input('Professor Name')
years = st.multiselect('Years', range(2000, 2025))

if st.button('Search'):
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
        st.write("No publications found.")
