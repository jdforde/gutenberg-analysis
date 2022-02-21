# gutenberg-analysis
Analysis of statistical data collected from all books on the Project Gutenberg website

## Web Scraping Overview
In order to perform analysis on the Project Gutenberg website, some preliminary web scraping must be done. Project Gutenberg books are indexed by an integer represneting their order in being added to the project. For example, https://www.gutenberg.org/ebooks/448 would represent the 448th book added to Project Gutenberg, which is *The Pyschology of Revolution* by Gustave Le Bon.

In general, we can scrape https://www.gutenberg.org/ebooks/x where *x* is an integer from 1 to (roughly) 67455.

This, however, would be incredibly inefficient. We speedup this process by using multithreading. With 5000, threads we scrape all of the books from Project Gutenburg and store the results in a dataframe for later analysis. 
