# Simple Web Crawler
A web crawler to identify potential customers and match their information with their LinkedIn account.

To optimise customer outreach this repository holds different web crawlers that retrieve information of potential interesting companies. The information that is retrieved by those crawlers is written to CSV-files. A second crawler uses the company information to look up their employees on LinkedIn and based on the number of contacts and job title saves their information. This information in turn is used for automated outreach.

*This is a quick set-up, which serves to speed up the work of the non-technical part of the team. In order to be fast, some of the crawlers were written with Beautiful Soup, while for others the heavier Selenium was used. The second refers mainly to Core Javascript featured webpages like LinkedIn.*
