# Movie Info Scraper

This script is used to scrape movie information and download links from various RSS feeds and display them in an HTML table.

## Dependencies

The following libraries are required to run this script:

-   `concurrent.futures`
-   `json`
-   `re`
-   `urllib.parse`
-   `feedparser`
-   `requests`
-   `bs4`
-   `jinja2`

## Usage

To use this script, follow these steps:

1. Update the `input/rssFeeds.json` file with the desired RSS feed URLs. The format of this file should be a dictionary where the keys are the names of the RSS feeds and the values are the URLs.

2. Run the script using `python main.py`.

3. The script will scrape movie information and download links from the specified RSS feeds, and generate an HTML table displaying this information. The table will be saved in the `output` folder as `outputHtml.html`.

## Customization

You can customize the appearance of the generated HTML table by modifying the `templates/TableTemplate.html` file. This file uses Jinja2 syntax to generate the table based on the movie data.

## Notes

-   The script will only include movies with 1080p, 2160p, or 4K in the title in the generated table.
-   The script will only include the first 5 actors for each movie in the generated table.
