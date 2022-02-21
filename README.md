# gutenberg-analysis
Analysis of statistical data collected from all books on the Project Gutenberg website

## Web Scraping Process
In order to perform analysis on the Project Gutenberg website, some preliminary web scraping must be done. Project Gutenberg books are indexed by an integer represneting their order in being added to the project. For example, https://www.gutenberg.org/ebooks/448 would represent the 448th book added to Project Gutenberg, which is *The Pyschology of Revolution* by Gustave Le Bon.

In general, we can scrape https://www.gutenberg.org/ebooks/x where *x* is an integer from 1 to (roughly) 67455.

This, however, would be incredibly inefficient. We speedup this process by using multithreading. With 5000, threads we scrape all of the books from Project Gutenburg and store the results in a dataframe for later analysis. 

## Data Frame Structure

Here is an example of two entires from the dataframe to illustrate the structure:

Title                 | Author         | Subject 1        | Subject 2      | Subject 3  | Downloads         | Word Count      | Language      | Release Date 
------------- | -------------  | ---------------  | -------------- | ---------- | ----------------- | --------------  | ------------  | -----------
Notes on the Iriquois  | Henry Rowe Schoolcraft  | Iriquois Indians     | Indians of North America -- New York (State)  | NA    | 72           | 96579         | English       | 2015-09-25
Nightmare Abbey | Thomas Love Peacock   | Humorous Stories    | Gothic fiction   | Postmodern    | 124           | 27380         | English       | 2006-02-01

- **Title** is a string representing the title of the book.
- **Author** is a string of the author or authors of the book. 'NA' if there is no author.
- **Subjects 1, 2, and 3** represent three subjects/genres of the particular book. Some entires only have 1 or 2 subjects listed. If there aren't three subjects, the remaining subjects are listed as NA.
- **Downloads** is an integer representing the number of downloads in the past 30 days. It is a good way to measure popularity of the book.
- **Word Count** is an integer representing the approximate word count of the book.
- **Language** is a string representing the language of the book.
- **Release Date** is a date object representing when the book was first published.
