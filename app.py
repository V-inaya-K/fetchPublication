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

# def get_publications_from_google_scholar(professor_name, years):
#     try:
#         search_query = scholarly.search_author(professor_name)
#         authors = list(search_query)  # iterate over the generator object and retrieve the results
#         print("Google Scholar API response:", authors)
#         publications = []
#         for author in authors:
#             if 'name' in author:
#                 similarity = fuzz.ratio(author['name'].lower(), professor_name.lower())
#                 if similarity > 80:  # if the similarity is greater than 80, we consider it a match
#                     scholarly.fill(author)
#                     pubs = author['publications']
#                     for pub in pubs:
#                         if 'year' in pub and str(pub['year']) in [str(year) for year in years]:
#                             publications.append({
#                                 'title': pub['bib']['title'],
#                                 'year': pub['year'],
#                                 'authors': [author['name'] for author in pub['authors']],
#                                 'citations': pub['num_citations']
#                             })
#                     time.sleep(1)  # add a delay of 1 second between requests
#         return publications
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return []

# def get_publications_from_dblp(professor_name, years):
#     url = f"https://dblp.org/search/publ/api?q={professor_name}&h=100&format=json"
#     response = requests.get(url)
#     data = response.json()
#     publications = data['result']['hits']['hit']
#     filtered_publications = []
#     for pub in publications:
#         if 'info' in pub and 'year' in pub['info'] and pub['info']['year'] in years:
#             filtered_publications.append({
#                 'title': pub['info']['title'],
#                 'year': pub['info']['year'],
#                 'authors': [author['text'] for author in pub['info']['authors']['author']],
#                 'citations': 0  # DBLP API does not provide citation count
#             })
#     return filtered_publications

# def get_publications(professor_name, years):
#     google_scholar_publications = get_publications_from_google_scholar(professor_name, years)
#     dblp_publications = get_publications_from_dblp(professor_name, years)
#     all_publications = google_scholar_publications + dblp_publications
#     print("Publications:", all_publications)
#     return all_publications

# st.title('Publication Record Tool')

# professor_name = st.text_input('Professor Name')
# years = st.multiselect('Years', range(2000, 2025))

# if st.button('Search'):
#     print("Professor's name:", professor_name)
#     print("Years:", years)
#     publications = get_publications(professor_name, years)
#     if publications:
#         df = pd.DataFrame(publications)
#         print("DataFrame:", df)
#         st.write(df)
#     else:
#         st.write("No publications found.")


# def get_publications_from_google_scholar(professor_name, years):
#     try:
#         search_query = scholarly.search_author(professor_name)
#         authors = list(search_query)  # iterate over the generator object and retrieve the results
#         print("Google Scholar API response:", authors)
#         publications = []
#         for author in authors:
#             similarity = fuzz.ratio(author['name'], professor_name)
#             if similarity > 80:  # if the similarity is greater than 80, we consider it a match
#                 scholarly.fill(author)
#                 pubs = author['publications']
#                 for pub in pubs:
#                     if 'year' in pub and pub['year'] in years:
#                         publications.append({
#                             'title': pub['bib']['title'],
#                             'year': pub['year'],
#                             'authors': [author['name'] for author in pub['authors']],
#                             'citations': pub['num_citations']
#                         })
#         return publications
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return []

# def get_publications_from_google_scholar(professor_name, years):
#     try:
#         search_query = scholarly.search_author(professor_name)
#         authors = list(search_query)  # iterate over the generator object and retrieve the results
#         print("Google Scholar API response:", authors)
#         publications = []
#         for author in authors:
#             if author['name'] == professor_name:
#                 scholarly.fill(author)
#                 pubs = author['publications']
#                 for pub in pubs:
#                     if 'year' in pub and pub['year'] in years:
#                         publications.append({
#                             'title': pub['bib']['title'],
#                             'year': pub['year'],
#                             'authors': [author['name'] for author in pub['authors']],
#                             'citations': pub['num_citations']
#                         })
#         return publications
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return []

# def get_publications_from_google_scholar(professor_name, years):
#     try:
#         search_query = scholarly.search_author(professor_name)
#         authors = list(search_query)  # iterate over the generator object and retrieve the results
#         print("Google Scholar API response:", authors)
#         if authors:
#             author = authors[0]
#             scholarly.fill(author)
#             publications = author['publications']
#             filtered_publications = []
#             for pub in publications:
#                 if 'year' in pub and pub['year'] in years:
#                     filtered_publications.append({
#                         'title': pub['bib']['title'],
#                         'year': pub['year'],
#                         'authors': [author['name'] for author in pub['authors']],
#                         'citations': pub['num_citations']
#                     })
#             return filtered_publications
#         else:
#             return []
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return []

# def get_publications_from_google_scholar(professor_name, years):
#     search_query = scholarly.search_author(professor_name)
#     try:
#         search_query = scholarly.search_author(professor_name)#
#         time.sleep(1)  # wait for 1 second to avoid hitting the rate limit
#         print("Google Scholar API response:", search_query)#
#         author = next(search_query)
#         search_query = scholarly.search_author(professor_name)#
#         print("Google Scholar API response:", search_query)#
#     except StopIteration:
#         return []
#     scholarly.fill(author)
#     publications = author['publications']
#     filtered_publications = []
#     for pub in publications:
#         if 'year' in pub and pub['year'] in years:
#             filtered_publications.append({
#                 'title': pub['bib']['title'],
#                 'year': pub['year'],
#                 'authors': [author['name'] for author in pub['authors']],
#                 'citations': pub['num_citations']
#             })
#     return filtered_publications


# def get_publications(professor_name, years):
#     google_scholar_publications = get_publications_from_google_scholar(professor_name, years)
#     dblp_publications = get_publications_from_dblp(professor_name, years)
#     all_publications = google_scholar_publications + dblp_publications
#     return all_publications


# if st.button('Search'):
#     publications = get_publications(professor_name, years)
#     if publications:
#         df = pd.DataFrame(publications)
#         st.write(df)
#     else:
#         st.write("No publications found.")
#---------------------------------------------------------------------------------------------------

# import streamlit as st
# import pandas as pd
# import requests
# from scholarly import scholarly

# def get_publications_from_google_scholar(professor_name, years):
#     search_query = scholarly.search_author(professor_name)
#     author = next(search_query)
#     scholarly.fill(author)
#     publications = author['publications']
#     filtered_publications = []
#     for pub in publications:
#         if 'year' in pub and pub['year'] in years:
#             filtered_publications.append({
#                 'title': pub['bib']['title'],
#                 'year': pub['year'],
#                 'authors': [author['name'] for author in pub['authors']],
#                 'citations': pub['num_citations']
#             })
#     return filtered_publications

# def get_publications_from_dblp(professor_name, years):
#     url = f"https://dblp.org/search/publ/api?q={professor_name}&h=100&format=json"
#     response = requests.get(url)
#     data = response.json()
#     publications = data['result']['hits']['hit']
#     filtered_publications = []
#     for pub in publications:
#         if 'info' in pub and 'year' in pub['info'] and pub['info']['year'] in years:
#             filtered_publications.append({
#                 'title': pub['info']['title'],
#                 'year': pub['info']['year'],
#                 'authors': [author['text'] for author in pub['info']['authors']['author']],
#                 'citations': 0  # DBLP API does not provide citation count
#             })
#     return filtered_publications

# def get_publications(professor_name, years):
#     google_scholar_publications = get_publications_from_google_scholar(professor_name, years)
#     dblp_publications = get_publications_from_dblp(professor_name, years)
#     all_publications = google_scholar_publications + dblp_publications
#     return all_publications

# st.title('Publication Record Tool')

# professor_name = st.text_input('Professor Name')
# years = st.multiselect('Years', range(2000, 2025))

# if st.button('Search'):
#     publications = get_publications(professor_name, years)
#     df = pd.DataFrame(publications)
#     st.write(df)



# import scrapy
# from scrapy.crawler import CrawlerProcess
# from bs4 import BeautifulSoup
# import requests

# class GoogleScholarSpider(scrapy.Spider):
#     name = "google_scholar"
#     start_urls = [
#         'https://scholar.google.com/scholar?q=python+scraping',
#     ]

#     def parse(self, response):
#         soup = BeautifulSoup(response.body, 'html.parser')
#         for result in soup.find_all('div', class_='gs_r'):
#             title = result.find('h3', class_='gs_rt').text.strip()
#             authors = result.find('div', class_='gs_a').text.strip()
#             publication_year = result.find('span', class_='gs_age').text.strip()
#             yield {
#                 'title': title,
#                 'authors': authors,
#                 'publication_year': publication_year,
#             }

# if __name__ == "__main__":
#     process = CrawlerProcess()
#     process.crawl(GoogleScholarSpider)
#     process.start()

# Error: Cannot Fetch from Google Scholar.
# Search query: <scholarly.publication_parser._SearchScholarIterator object at 0x000002534D7602E0>
# Google Scholar results: []
# Proxy success: True
# Proxy generator: <scholarly._proxy_generator.ProxyGenerator object at 0x000002534EF58490>


# import streamlit as st
# from scholarly import scholarly, ProxyGenerator

# # Initialize the app
# st.title("Professor Publication Tool")

# # Input fields for professor's name and years
# professor_name = st.text_input("Professor's Name")
# start_year = st.number_input("Start Year", min_value=1900, max_value=2024)
# end_year = st.number_input("End Year", min_value=1900, max_value=2024)

# # Set up a proxy
# pg = ProxyGenerator()
# success = pg.FreeProxies()
# scholarly.use_proxy(pg)

# # Button to trigger the search
# if st.button("Search"):
#     try:
#         # Search Google Scholar
#         search_query = scholarly.search_pubs(professor_name)
#         google_scholar_results = []
#         for result in search_query:
#             if 'pub_year' in result and start_year <= int(result['pub_year']) <= end_year:
#                 google_scholar_results.append(result)

#         # Display results
#         st.write("Publications:")
#         for result in google_scholar_results:
#             st.write(result.get('title', ''))
#             st.write(result.get('author', ''))
#             st.write(result.get('pub_year', ''))
#             st.write(result.get('pub_conference', ''))
#             st.write(result.get('url', ''))
#             st.write("---")
#     except Exception as e:
#         st.error("Error: " + str(e))
#         print("Error:", e)
#         print("Search query:", search_query)
#         print("Google Scholar results:", google_scholar_results)
#         print("Proxy success:", success)
#         print("Proxy generator:", pg)


# import streamlit as st
# from scholarly import scholarly, ProxyGenerator

# # Initialize the app
# st.title("Professor Publication Tool")

# # Input fields for professor's name and years
# professor_name = st.text_input("Professor's Name")
# start_year = st.number_input("Start Year", min_value=1900, max_value=2024)
# end_year = st.number_input("End Year", min_value=1900, max_value=2024)

# # Set up a proxy
# pg = ProxyGenerator()
# success = pg.FreeProxies()
# scholarly.use_proxy(pg)

# # Button to trigger the search
# if st.button("Search"):
#     try:
#         # Search Google Scholar
#         search_query = scholarly.search_pubs(professor_name)
#         google_scholar_results = []
#         for result in search_query:
#             if 'pub_year' in result and start_year <= int(result['pub_year']) <= end_year:
#                 google_scholar_results.append(result)

#         # Display results
#         st.write("Publications:")
#         for result in google_scholar_results:
#             st.write(result.get('title', ''))
#             st.write(result.get('author', ''))
#             st.write(result.get('pub_year', ''))
#             st.write(result.get('pub_conference', ''))
#             st.write(result.get('url', ''))
#             st.write("---")
#     except Exception as e:
#         st.error("Error: " + str(e))


# import streamlit as st
# from scholarly import scholarly

# # Initialize the app
# st.title("Professor Publication Tool")

# # Input fields for professor's name and years
# professor_name = st.text_input("Professor's Name")
# start_year = st.number_input("Start Year", min_value=1900, max_value=2024)
# end_year = st.number_input("End Year", min_value=1900, max_value=2024)

# # Button to trigger the search
# if st.button("Search"):
#     try:
#         # Search Google Scholar
#         search_query = scholarly.search_pubs(professor_name)
#         google_scholar_results = []
#         for result in search_query:
#             if 'pub_year' in result and start_year <= int(result['pub_year']) <= end_year:
#                 google_scholar_results.append(result)

#         # Display results
#         st.write("Publications:")
#         for result in google_scholar_results:
#             st.write(result.get('title', ''))
#             st.write(result.get('author', ''))
#             st.write(result.get('pub_year', ''))
#             st.write(result.get('pub_conference', ''))
#             st.write(result.get('url', ''))
#             st.write("---")
#     except Exception as e:
#         st.error("Error: " + str(e))
# import streamlit as st
# from scholarly import scholarly

# # Initialize the app
# st.title("Professor Publication Tool")

# # Input fields for professor's name and years
# professor_name = st.text_input("Professor's Name")
# start_year = st.number_input("Start Year", min_value=1900, max_value=2024)
# end_year = st.number_input("End Year", min_value=1900, max_value=2024)

# # Button to trigger the search
# if st.button("Search"):
#     # Search Google Scholar
#     search_query = scholarly.search_pubs(professor_name)
#     google_scholar_results = []
#     for result in search_query:
#         if start_year <= result.year <= end_year:
#             google_scholar_results.append(result)

#     # Display results
#     st.write("Publications:")
#     for result in google_scholar_results:
#         st.write(result.title)
#         st.write(result.authors)
#         st.write(result.year)
#         st.write(result.publication)
#         st.write(result.url)
#         st.write("---")



# import streamlit as st
# from scholarly import scholarly
# from dblp import dblp

# # Initialize the app
# st.title("Professor Publication Tool")

# # Input fields for professor's name and years
# professor_name = st.text_input("Professor's Name")
# start_year = st.number_input("Start Year", min_value=1900, max_value=2024)
# end_year = st.number_input("End Year", min_value=1900, max_value=2024)

# # Button to trigger the search
# if st.button("Search"):
#     # Search Google Scholar
#     search_query = scholarly.search_pubs(professor_name)
#     google_scholar_results = []
#     for result in search_query:
#         if start_year <= result.year <= end_year:
#             google_scholar_results.append(result)

#     # Search DBLP
#     dblp_results = dblp.search(professor_name, start_year, end_year)

#     # Convert DBLP results to a consistent format
#     dblp_results_converted = []
#     for result in dblp_results:
#         publication = {
#             'title': result.get('title', ''),
#             'authors': result.get('authors', []),
#             'year': result.get('year', ''),
#             'publication': result.get('publication', ''),
#             'url': result.get('url', '')
#         }
#         dblp_results_converted.append(publication)

#     # Combine results
#     results = google_scholar_results + dblp_results_converted

#     # Display results
#     st.write("Publications:")
#     for result in results:
#         st.write(result.get('title', ''))
#         st.write(result.get('authors', ''))
#         st.write(result.get('year', ''))
#         st.write(result.get('publication', ''))
#         st.write(result.get('url', ''))
#         st.write("---")




# # import streamlit as st
# # from scholarly import scholarly
# # #from dblp import dblp

# # # Initialize the app
# # st.title("Professor Publication Tool")

# # # Input fields for professor's name and years
# # professor_name = st.text_input("Professor's Name")
# # start_year = st.number_input("Start Year", min_value=1900, max_value=2024)
# # end_year = st.number_input("End Year", min_value=1900, max_value=2024)

# # # Button to trigger the search
# # if st.button("Search"):
# #     # Search Google Scholar
# #     search_query = scholarly.search_pubs(professor_name)
# #     google_scholar_results = []
# #     for result in search_query:
# #         if start_year <= result.year <= end_year:
# #             google_scholar_results.append(result)

# #     # Search DBLP
# #     dblp_results = dblp.search(professor_name, start_year, end_year)

# #     # Combine results
# #     results = google_scholar_results + dblp_results

# #     # Display results
# #     st.write("Publications:")
# #     for result in results:
# #         st.write(result.title)
# #         st.write(result.authors)
# #         st.write(result.year)
# #         st.write(result.publication)
# #         st.write(result.url)
# #         st.write("---")