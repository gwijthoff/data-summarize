# "Data, Summarize"

**An experiment in concurrent text analysis and typesetting.**

The cool thing about writing Python in DrawBot is that you can simultaneously analyze your data and typeset the results. This repo contains a Python script `data_summarize.py` that loops through a collection of books from HathiTrust Research Center, analyzes the text of those books, and prints the output in PNG and PDF. Each **text analysis broadside** provides a snapshot of some quantitative measures of the book.

The Python script is run in [DrawBot](https://drawbot.com/), an open-source integrated development environment for Python often used by graphic designers for creating fonts and kinetic typography. [Extracted Features](https://programminghistorian.org/en/lessons/text-mining-with-extracted-features) is a data format devised by HTRC in order to enable text analysis on post-1926 books still under copyright.

When run in DrawBot, `data_summarize.py` takes the Extracted Features file for one book, pulls its metadata, takes a sample of random tokens, performs [TF-IDF](https://programminghistorian.org/en/lessons/analyzing-documents-with-tfidf) analysis, and calculates the appropriate font size for author name and title based on the number of letters that have to fit into a prescribed width. It then prints the results in both PNG and PDF. Places are noted in the script where the broadside's design, font, and colors can be customized to suit the genre or period of the books you're analyzing.

For this demonstration, I'm using HTRC's collection of 3,236 English-language speculative fiction novels of the 20th century. For more on the speculative fiction texts hosted by HTRC and to replicate the process I took to download them, you can use [these Python notebooks](https://github.com/gwijthoff/HTRC_SF_experiments).

<p align="center">
    <img src="output/Delany_1967_THE%20EINSTEIN%20INTERSECTION%20.png" alt="Broadside displaying quantitative measures of Samuel R. Delany's The Einstein Intersection." />
</p>

|                           |                           |
| ------------------------- | ------------------------- |
| ![](output/Atwood_1986_THE%20HANDMAID'S%20TALE%20.png)  |  ![](output/Silverberg_1969_ACROSS%20A%20BILLION%20YEARS.png) |
| ![](output/Heinlein_1952_THE%20ROLLING%20STONES%20.png)  |  ![](output/Brite_1992_LOST%20SOULS%20.png) |

<p align="center">
    <img src="summarizeplease.gif" alt="Commander Data quickly thumbing pages of a novel before his eyes in order to scan and summarize its text." />
</p>
