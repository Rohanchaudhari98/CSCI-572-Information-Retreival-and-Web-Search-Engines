# import json
# import time
# import requests
# from random import randint
# from bs4 import BeautifulSoup
# from urllib.parse import unquote

# USER_AGENT = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}
# count = 0

# class SearchEngine:
#     def __init__(self):
#         pass

#     @staticmethod
#     def search(query, sleep=True):
#         global count
#         if sleep:  # Prevents loading too many pages too soon
#             time.sleep(randint(10, 50))
#         temp_url = "+".join(query.split())  # For adding + between words for the query
#         url = 'https://www.duckduckgo.com/html/?q=' + temp_url + "&count=30"
#         count = count + 1
#         print(count)
#         print(url)
#         soup = BeautifulSoup(requests.get(url, headers=USER_AGENT).text, "html.parser")
#         new_results = SearchEngine.scrape_search_result(soup)
#         print(new_results)
#         print(len(new_results))
#         return new_results

#     @staticmethod
#     def scrape_search_result(soup):
#         raw_results = soup.find_all("a", attrs={"class": "result__a"})
#         return SearchEngine.add_url_to_results(raw_results)

#     @staticmethod
#     def add_url_to_results(raw_results):
#         results = []
#         for result in raw_results:
#             # print(result)
#             url = result.get('href')
#             if url not in results:  # Check for any duplicate link
#                 results.append(url)
#             if len(results) == 10:  # If we already have 10 different results, quit
#                 break
#         return results

#     # @staticmethod
#     # def find_url(result):
#     #     href = result.get("href")
#     #     start_location = href.find("RU=")
#     #     end_location = href.find("/RK")
#     #     url = unquote(href[start_location: end_location])
#     #     return url


# def main():
#     queries, google_results = read_files()
#     stats, yahoo_results = perform_tasks(queries, google_results)
#     calculate_avg_stats(stats)
#     write_result(stats, yahoo_results)


# def read_files():
#     with open("data/100QueriesSet4.txt", "r") as f:
#         queries = f.readlines()
#     with open("data/Google_Result4.json", "r") as f:
#         google_results = json.load(f)
#     return queries, google_results


# def perform_tasks(queries, google_results):
#     yahoo_results = {}
#     stats = {}
#     for _, query in enumerate(queries):
#         # Task 1: Scraping results from Yahoo!
#         query = query.rstrip()
#         yahoo_results[query] = SearchEngine.search(query)

#         # Task 2: Determining the Percent Overlap and the Spearman Coefficient
#         matching_url = get_matching_url(query, google_results, yahoo_results)
#         rho = calculate_rho(matching_url)
#         stats[query] = {"Overlap": len(matching_url), "Percent": len(matching_url) / 10, "Rho": rho}
#     return stats, yahoo_results


# def get_matching_url(query, google_results, yahoo_results):
#     matching_url = []
#     for yahoo_index, yahoo_url in enumerate(yahoo_results[query]):
#         yahoo_url = manipulate_url(yahoo_url)
#         for google_index, google_url in enumerate(google_results[query]):
#             google_url = manipulate_url(google_url)
#             if yahoo_url == google_url:
#                 matching_url.append((google_index, yahoo_index))
#     return matching_url


# def manipulate_url(url):
#     # Ignore "https://" and "http://" in the URL
#     index = url.find("//")
#     if index > -1:
#         url = url[index + 2:]
#     # Ignore "www." in the URL
#     if "www." in url:
#         url = url[4:]
#     # Ignore "/" at the end of the URL
#     if url[-1] == "/":
#         url = url[:-1]
#     return url.lower()


# def calculate_rho(matching_url):
#     # If there is no matching, Spearman coefficient is 0
#     if len(matching_url) == 0:
#         coefficient = 0
#     # If there is exactly 1 matching
#     elif len(matching_url) == 1:
#         # If Google index and Yahoo index are the same, Spearman coefficient is 1, Otherwise, 0.
#         if matching_url[0][0] == matching_url[0][1]:
#             coefficient = 1
#         else:
#             coefficient = 0
#     else:
#         difference = sum([(a - b) ** 2 for a, b in matching_url])
#         coefficient = 1 - ((6 * difference) / (len(matching_url) * (len(matching_url) ** 2 - 1)))
#     return coefficient


# def calculate_avg_stats(stats):
#     avg_overlap, avg_percent_overlap, avg_coefficient = 0, 0, 0
#     for _, value in stats.items():
#         avg_overlap += value["Overlap"] / 100
#         avg_percent_overlap += value["Percent"] / 100
#         avg_coefficient += value["Rho"] / 100
#     stats["Averages"] = {"Overlap": avg_overlap, "Percent": avg_percent_overlap, "Rho": avg_coefficient}


# def write_result(stats, yahoo_results):
#     with open("hw1.json", "w") as f:
#         json.dump(yahoo_results, f, indent = 6)
#     with open("hw1.csv", "w") as f:
#         f.write("Queries, Number of Overlapping Results, Percent Overlap, Spearman Coefficient\n")
#         cnt = 0
#         for query_number, values in stats.items():
#             cnt = cnt + 1
#             f.write(f"Query {cnt}, {values['Overlap']}, {values['Percent']}, {values['Rho']}\n")


# main()


from bs4 import BeautifulSoup
from time import sleep as sleeptime
import requests
import json
import csv
from random import randint
from html.parser import HTMLParser

USER_AGENT = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


class SearchEngine:
    @staticmethod
    def search(query, sleep=True):
        if sleep:  # Prevents loading too many pages too soon
            sleeptime(randint(7, 20))
        temp_url = '+'.join(query.split())  # for adding + between words for the query
        url = 'https://www.duckduckgo.com/html/?q=' + temp_url
        soup = BeautifulSoup(requests.get(url, headers=USER_AGENT).text, "html.parser")
        new_results = SearchEngine.scrape_search_result(soup)
        return new_results

    @staticmethod
    def scrape_search_result(soup):
        raw_results = soup.find_all("a", attrs={"class": "result__a"})
        results = []
        seen_links = set()
        # implement a check to get only 10 results and also check that URLs must not be duplicated
        for result in raw_results:
            link = result.get('href')
            if link not in seen_links:
                results.append(link)
                seen_links.add(link)
            if len(results) == 10:
                break
        return results


class Crawler:
    def __main__(self):
        queries = []
        with open("100QueriesSet4.txt", "r") as file:
            for query in file:
                queries.append(query.rstrip("? \n"))

        main_results = {}
        for f, query in enumerate(queries):
            main_results[query] = SearchEngine.search(query, True)
            print(f)
            print(len(main_results[query]))
            if len(main_results[query]) != 10:
                print("Noooooooooooooooooooooooooooooooooo :(")
            print()

        with open("hw1.json", "w") as file:
            json.dump(main_results, file, indent=4)

        query_stats = []

        with open("Google_Result4.json", "r") as file:
            ref_results = json.load(file)

        total_overlaps, total_percent, total_rho = 0, 0, 0
        for idx, query in enumerate(queries):
            main_links = main_results[query]
            ref_links = ref_results[query]

            main_links_map = {}
            for pos, val in enumerate(main_links):
                val = self.trimUrl(val)
                main_links_map[val] = pos

            overlaps, sum = 0, 0
            overlap_match = False
            for pos, val in enumerate(ref_links):
                val = self.trimUrl(val)
                if val in main_links_map:
                    overlaps += 1
                    sum += ((pos - main_links_map[val]) ** 2)
                    if pos == main_links_map[val]:
                        overlap_match = True
                    else:
                        overlap_match = False

            if overlaps == 0:
                rho = 0
            elif overlaps == 1:
                rho = 1 if overlap_match else 0
            else:
                rho = 1 - ((6 * sum) / (overlaps * (overlaps ** 2 - 1)))

            query_stats.append(["Query"+ " " +str(idx+1), overlaps, float((overlaps/len(ref_links))*100), rho])
            total_overlaps += overlaps
            total_percent += float((overlaps/len(ref_links))*100)
            total_rho += rho

        with open("hw1.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Queries", "No of Overlapping Results", "Percent Overlap", "Spearman Coefficient"])
            writer.writerows(query_stats)
            writer.writerow(["Averages", total_overlaps/len(queries), total_percent/len(queries), total_rho/len(queries)])

    def trimUrl(self, link):
        return link.rstrip(" /").replace("www.", "").replace("https://", "").replace("http://", "")

robot = Crawler()
robot.__main__()