# WebCrawler
Our web crawler crawls a site, extracts the URLs from the site, and produces a list of those URLs. Currently, I am restricting my crawler such that it should not crawl outside of the domain for the seed URL, but should record URLs from any links to external pages in the list. These urls will be printed in the destination file as given by the user.

The crawler can be run as :

python WebCrawler.py <seed_url> <dest_file>
