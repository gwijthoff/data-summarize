# "Data, Summarize"

**An experiment in concurrent text analysis and typesetting.**

The cool thing about writing Python in DrawBot is that you can simultaneously analyze your data and typeset the results. This repo contains a Python script [`data_summarize.py`](data_summarize.py) that loops through a collection of books in HathiTrust, analyzes the text of those books, and prints the output in PNG and PDF. Each **text analysis broadside** provides a snapshot of some quantitative measures of the book.

The Python script is run in [DrawBot](https://drawbot.com/), an open-source integrated development environment for Python often used by graphic designers for creating fonts and kinetic typography. [Extracted Features](https://programminghistorian.org/en/lessons/text-mining-with-extracted-features) is a data format devised by HathiTrust Research Center in order to enable text analysis on post-1926 books still under copyright.

When run in DrawBot, [`data_summarize.py`](data_summarize.py) takes the Extracted Features file for each of the ten books listed by HathiTrust ID in [`EF_files.txt`](EF_files.txt). It then pulls the metadata for each book, takes a sample of random tokens, performs [TF-IDF](https://programminghistorian.org/en/lessons/analyzing-documents-with-tfidf) analysis, and calculates the appropriate font size for author name and title based on the letters that have to fit into a prescribed width.

Places are noted in the script where the broadside's design, font, and colors can be customized to suit the genre or period of the books you're analyzing.

<p align="center">
    <img src="output/Delany_1967_THE%20EINSTEIN%20INTERSECTION%20.png" alt="Broadside displaying quantitative measures of Samuel R. Delany's The Einstein Intersection." />
</p>

|                           |                           |
| ------------------------- | ------------------------- |
| ![](output/Atwood_1986_THE%20HANDMAID'S%20TALE%20.png)  |  ![](output/Butler_1980_WILD%20SEED%20.png) |
| ![](output/Asimov_1951_FOUNDATION.png)  |  ![](output/Brite_1992_LOST%20SOULS%20.png) |

<p align="center">
    <img src="summarizeplease.gif" alt="Commander Data quickly thumbing pages of a novel before his eyes in order to scan and summarize its text." />
</p>

# Requirements

- [DrawBot](https://drawbot.com/content/download.html), an open source IDE that unfortunately only runs on Mac. For an excellent guidebook to DrawBot, see Roberto Arista's [*Python for Designers*](https://www.pythonfordesigners.com/)
- the following Python libraries, installed via the command line with `pip install nltk htrc-feature-reader numpy sklearn pandas`
    - Natural Language Toolkit [(NLTK)](https://www.nltk.org/install.html) for removing stopwords
    - HTRC FeatureReader
    - [numpy](https://numpy.org/)
    - [sklearn](https://sklearn.org/)
    - [pandas](https://pandas.pydata.org/)
- Fonts: Futura and Hoefler Text will already be installed for Mac users. But I also use [Fira Code](https://github.com/tonsky/FiraCode), which will need to be downloaded and installed. Or you can specify any other fonts on your system.

# Usage

Download a .zip of this repository, unzip, and open the folder. Open the DrawBot application. File -> Open -> `data_summarize.py`. Click "Run". The script will loop through each of the ten HathiTrust IDs listed in `EF_files.txt`, and should take about 45 seconds to finish. PNG and PDF broadsides for each book will be saved to the `/output` directory.

To analyze and print broadsides for different books, you can replace the HathiTrust IDs in `EF_files.txt` with any of the 17.1 million books that are included in the Extracted Features dataset. (Not every catalog record on HathiTrust will be included in Extracted Features.) Just [search for your books](https://catalog.hathitrust.org/Search/Advanced) on HathiTrust and find the HTID at the end of that book's URL, i.e. the HTID for `https://babel.hathitrust.org/cgi/pt?id=uc1.32106016749274` would be `uc1.32106016749274`.
