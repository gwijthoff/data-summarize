# ==== COLOR CONVERSION ====

# rgb converter
rgb = 255
# cosmic latte
latte = (255/rgb, 248/rgb, 231/rgb)
# off-black
offBlack = (17/rgb, 17/rgb, 17/rgb)
# accent red
vermilion = (227/rgb, 66/rgb, 52/rgb)

# ==== FONTS ====

headFont = 'Futura-Bold'
tagFont = 'Futura-Medium'
bodyFont = 'HoeflerText-Regular'
monoFont = 'Fira Code'

font('HoeflerText-Regular')
defaultSize = 50
noteSize = defaultSize/2
textFill = 0

# ==== PULL NOVEL DATA ====

import os

#  create a list of HathiTrust IDs from paths.txt
my_file = open('EF_files.txt')
list = my_file.readlines()
items = []
for i in list:
    items.append(i)

# remove the \n (newline) character from that list
paths = [x[:-1] for x in items]

# import HTRC Feature Reader
from htrc_features import Volume

for item in paths:
    vol = Volume(item)

    # ==== LAYOUT ====

    fill(*latte) # page color
    rect(0, 0, width(), height()) # page size 

    pmargin = 100 # page margins
    tmargin = 25 # margins of text inside box
    
    # size of centered box minus page margins
    w = width()/2 - pmargin
    h = height()/2 - pmargin

    # ==== BOX 1: UPPER LEFT ====

    # ---- bibliographic data ----

    # convert novel data to strings
    # list -> string and .partition for removing first name and anything else like birth/death dates after a comma
    author=''.join(map(str,vol.author))
    authorShort = author.partition(',')[0]
    title = f'{vol.title}'
    title = title.partition('/')[0] # remove any characters after the title
    title = title.partition('.')[0]
    # title = title.partition(',')[0]
    title = title.upper() # uppercase
    pubyear = f'{vol.year}'
    publisher = f'{vol.publisher}'
    isbn = f'{vol.isbn}'

    # ---- typesetting ----

    ## calculate author font size
    font(headFont)
    targetWidth = 350 # size of each text box -tmargin
    fontSize(defaultSize)
    textWidth, textHeight = textSize(f'{authorShort}\n')
    calcAuthorSize = defaultSize * (targetWidth/textWidth)

    ## calculate title font size
    targetWidth = 350 # size of each text box -tmargin
    fontSize(defaultSize)
    textWidth, textHeight = textSize(f'{title}\n')
    calcTitleSize = defaultSize * (targetWidth/textWidth)

    fill(*offBlack) # font color
    fontSize(defaultSize)
    a = FormattedString()
    a.font(headFont)
    a.lineHeight(90)
    a.fontSize(calcAuthorSize)
    # turn on lining figures, ligatures, misc opentype features
    a.openTypeFeatures(dlig=True)
    a += f'{authorShort}\n'
    a.fontSize(calcTitleSize)
    a += f'{title}\n'
    a.fontSize(defaultSize)
    # find SET_IN year with wikidata, and match line width to those two dates side by side. Some will be a year, others will be a decade with an 's'
    a += f'{pubyear }'
    textBox(a, ((pmargin+tmargin), (width()/2 + tmargin), (w - tmargin*2), (h - tmargin*2)))

    # ==== BOX 2: UPPER RIGHT ====

    # ---- random sample of tokens ----
    
    tokens = vol.tokens()
    
    # push stopwords to a list
    from nltk.corpus import stopwords
    stop = stopwords.words('english')
    
    # remove stopwords from list of tokens
    words = [x for x in tokens if x not in stop]
    
    words_no_digits = [x for x in words if not (x.isdigit() 
                                         or x[0] == '-' and x[1:].isdigit())]
    
    # shuffle the tokens each time
    import random
    random.shuffle(words_no_digits)
    
    # convert token list to string
    word_sample=', '.join(map(str,words_no_digits))
    
    # ---- typesetting ----

    font(bodyFont)
    fill(*offBlack) # font color
    fontSize(noteSize)
    textBox(f'{word_sample}', ((width()/2)+tmargin, (height()/2 + tmargin), (w - tmargin*2), (h - tmargin*2)), align="justified")

    # ==== BOX 3: LOWER LEFT ====

    # ---- TF-IDF ----
    
    import pandas as pd

    # pull HathiTrust data through list of IDs
    my_ids = open('EF_files.txt')
    id_list_raw = my_ids.readlines()
    ids = []
    for i in id_list_raw:
        ids.append(i)

    # remove the \n character from that list
    id_list = [x[:-1] for x in ids]

    # loop through list of volume IDs and make a DF including extracted features,
    # book title, and publication year, then make a list of all DFs
    all_tokens = []
    for hathi_id in id_list:
        #Read in HathiTrust volume
        volume = Volume(hathi_id)
        #Make dataframe from token list -- do not include part of speech, sections, or case sensitivity
        token_df = volume.tokenlist(case=False, pos=False, drop_section=True, pages=False)
        #Add book column
        token_df['book'] = volume.title
        #Add publication year column
        token_df['year'] = volume.year
        all_tokens.append(token_df)

    # H/T Melanie Walsh for the TF-IDF formula https://melaniewalsh.github.io/Intro-Cultural-Analytics/05-Text-Analysis/02-TF-IDF-HathiTrust.html
    # concatenate the list of DFs
    sftoken_df = pd.concat(all_tokens)
    # Change from multi-level index to regular index
    sfdf_flattened = sftoken_df.reset_index()

    # drop all tokens from the df that are in my list of stopwords above
    sfdf_flattened = sfdf_flattened.drop(sfdf_flattened[sfdf_flattened['lowercase'].isin(stop)].index)

    # remove all punctuation by using a regular expression [^A-Za-z\s]
    # that matches anything not a letter and drops it from the DF
    sfdf_flattened = sfdf_flattened.drop(sfdf_flattened[sfdf_flattened['lowercase'].str.contains('[^A-Za-z\s]', regex=True)].index)

    # TERM FREQUENCY w/ renamed columns
    word_frequency_df = sfdf_flattened.rename(columns={'lowercase': 'term','count': 'term_frequency'})

    # DOCUMENT FREQUENCY w/ renamed columns
    document_frequency_df = (word_frequency_df.groupby(['book','term']).size().unstack()).sum().reset_index()
    document_frequency_df = document_frequency_df.rename(columns={0: 'document_frequency'})

    # merge word frequency + document frequency DFs
    word_frequency_df = word_frequency_df.merge(document_frequency_df)

    # calculate total number of documents in the collection by counting
    # unique values in story column
    total_number_of_docs = sfdf_flattened['book'].nunique()

    # calculate inverse document frequency
    # using default version from scikit-learn library, which adds 'smoothing'
    # to inverse document frequency

    # this code adds a column `idf` to the df
    # that's calculated off other existing columns in the df
    import numpy as np
    word_frequency_df['idf'] = np.log((1 + total_number_of_docs) / (1 + word_frequency_df['document_frequency'])) + 1

    # now calculate tf-idf by multiplying term frequency and inverse document frequency together
    word_frequency_df['tfidf'] = word_frequency_df['term_frequency'] * word_frequency_df['idf']

    # normalize these values with the scikit-learn library
    from sklearn import preprocessing
    word_frequency_df['tfidf_normalized'] = preprocessing.normalize(word_frequency_df[['tfidf']], axis=0, norm='l2')

    matches = word_frequency_df[word_frequency_df['book'].str.contains(vol.title)].sort_values(by=['tfidf_normalized'], ascending=[False]).head(6)

    matches = matches.rename(columns={'tfidf_normalized': 'TF-IDF','term': 'TERM'})
    cols = ['TERM', 'TF-IDF']
    matches = matches[cols].set_index('TERM')

    # ---- typesetting ----

    font(monoFont)
    fill(*vermilion) # red text
    fontSize(noteSize)
    textBox(f'{matches}', ((pmargin+tmargin), (pmargin+tmargin), (w - tmargin*2), (h - tmargin*2)), align="justified")

    # ==== BOX 4: LOWER RIGHT ====

    # ---- bibliographic data ----
    url = f'{vol.handle_url}'
    pgs = f'{vol.page_count}'
    place = f'{vol.pub_place}'
    oclc = f'{vol.oclc}'

    # ---- unique tokens / vocab size ----
    bag = vol.tokens()
    vocab = len(bag)

    # ---- typesetting ----

    fill(*offBlack)
    m = FormattedString()
    m.lineHeight(30)
    m.fontSize(noteSize/1.55)

    m.font(tagFont)
    m += f'Author            '
    m.font(bodyFont)
    m += f' {author}\n'
    m.font(tagFont)
    m += f'Publisher         '
    m.font(bodyFont)
    m += f'{publisher}\n'
    m.font(tagFont)
    m += f'Place              '
    m.font(bodyFont)
    m += f'{place}\n'
    m.font(tagFont)
    m += f'Length             '
    m.font(bodyFont)
    m += f'{pgs}pp.\n'
    m.font(tagFont)
    m += f'Vocab size      '
    m.font(bodyFont)
    m += f'{vocab} unique words\n'
    m.font(tagFont)
    m += f'ISBN              '
    m.font(bodyFont)
    m += f'{isbn}\n'
    m.font(tagFont)
    m += f'OCLC ID         '
    m.font(bodyFont)
    m += f'{oclc}\n'
    m.font(tagFont)
    m += f'HTRC link\n'
    m.font(bodyFont)
    m += f'{url}\n'

    textBox(m, ((width()/2)+tmargin, (pmargin + tmargin), (w - tmargin*2), (h - tmargin*2)), align="justified")

    # ==== LABELS ====

    with savedState():
        c2 = FormattedString()
        c2.fontSize(noteSize/1.3)
        c2.font(tagFont)
        c2.fill(*offBlack)
        # c2.underline('single')
        c2 += 'DISTINCTIVE TOKENS'
        translate(215, 60)
        rotate(90)
        # draw something
        textBox(c2, ((pmargin+tmargin), (pmargin+tmargin), 200, 38))

    with savedState():
        c1 = FormattedString()
        c1.fontSize(noteSize/1.3)
        c1.font(tagFont)
        c1.fill(*vermilion)
        # c1.underline('single')
        c1 += 'A SAMPLE OF TOKENS'
        translate(360, 1330)
        rotate(270)
        textBox(c1, ((width()/2)+tmargin, (height()/2 + tmargin), 433, 66))

    # ==== FOOTER ====

    font(headFont)
    fontSize(noteSize/1.4)
    footer = '"DATA, SUMMARIZE"'
    textWidth, textHeight = textSize(footer)
    textBox(footer, ((width()/2)-(textWidth/2), (pmargin/2.5), textWidth, textHeight), align="center")

    # ==== SAVE ====

    saveImage(f'output/{authorShort}_{pubyear}_{title}.pdf')
    saveImage(f'output/{authorShort}_{pubyear}_{title}.png', imageResolution=144)

    print (f'just printed {authorShort}\'s {title}.')

