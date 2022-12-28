# Movie Info Scraper for Torrenting

This is a Python script that scrapes movie information from IMDb using a list of RSS feeds and stores the information in a JSON file. The script also generates an HTML file using a Jinja2 template to display the movie information in a table format.

## Dependencies

-   Python 3.5 or higher
-   [feedparser](https://pypi.org/project/feedparser/)
-   [requests](https://pypi.org/project/requests/)
-   [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
-   [Jinja2](https://pypi.org/project/Jinja2/)

## Usage

1.  Install the dependencies using pip:

    `pip install feedparser requests beautifulsoup4 Jinja2`

2.  Add the RSS feed URLs to the file in the directory. The file should have the following format: <br>
    `{
"RSS Feed Name": "RSS Feed URL",
"Another RSS Feed": "Another RSS Feed URL"
}`

3.  Run the script: <br>
    `python3 main.py`

The movie information will be stored in the file and the HTML file will be generated in the root directory as `renderedHtml.html`

## Functions

The following functions are defined in the script:

-   `get_movie_name_from_rss_string(rssStr)`: Extracts the movie name from the RSS entry string.
-   `get_movie_details_from_rss(rssUrl)`: Returns a set of movie names from the RSS feed at the given URL.
-   `make_async_func(func)`: A decorator function that allows the given function to be used with the `concurrent.futures` module.
-   `get_movie_info(movie_title)`: Returns a dictionary containing the movie's title, synopsis, and a list of the top 5 cast members.
-   `get_rss_movie_info(rssName, rssUrl)`: Returns a dictionary of movie information for all movies in the RSS feed at the given URL.

## Template

The HTML template used to generate the table is stored in the directory as `TableTemplate.html` The template uses Jinja2 syntax to insert the movie information into the table.

## TODO

-   Currently I am only retreiving the data from IMDB and showing it in the table. I plan on adding a new column in the table with a download link that either downloads the .torrent file or the magnet.
-   For movies with multiple format, logic to determine highest quality must be decided
