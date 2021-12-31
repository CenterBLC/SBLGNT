import os
import re
import collections
import json
import csv
# from glob import glob
from tf.fabric import Fabric
from tf.convert.walker import CV
# from tf.compose import modify


source_dirs = 'input'
output_dirs = 'output'

bo2book = {line.split()[0]:line.split()[1] for line in '''
MT Matthew
MR Mark
LU Luke
JOH John
AC Acts
RO Romans
1CO 1_Corinthians
2CO 2_Corinthians
GA Galatians
EPH Ephesians
PHP Philippians
COL Colossians
1TH 1_Thessalonians
2TH 2_Thessalonians
1TI 1_Timothy
2TI 2_Timothy
TIT Titus
PHM Philemon
HEB Hebrews
JAS James
1PE 1_Peter
2PE 2_Peter
1JO 1_John
2JO 2_John
3JO 3_John
JUDE Jude
RE Revelation
'''.split('\n') if line}

# patts = {'section': re.compile('(\d*):(\d*)\.(\d*)')}

def director(cv):
        
    '''
    Walks through Tischendorf and triggers
    slot and node creation events.
    '''
        
    # process books in order
    for bo, book in bo2book.items():
        
        book_loc = os.path.join(source_dirs, f'{bo}.txt')
        
        print(f'\thandling {book_loc}...')
        
        with open(book_loc, 'r', encoding="utf8") as infile:
            text = [w for w in infile.read().split('\n') if w]
            
        this_book = cv.node('book')
        cv.feature(this_book, book=book)
            
        # keep track of when to trigger paragraph, chapter, and verse objects
        # para_track = 1 # keep counts of paragraphs
        prev_chap = 1 # start at 1
        prev_verse = 1 # start at 1
        # prev_subverse = ''
        sentence_track = 1
        sentence_done = False
        clause_track = 1
        clause_done = False
        wrdnum = 0 # start at 0
        
        this_chap = cv.node('chapter')
        this_sentence = cv.node('sentence')
        this_clause = cv.node('clause')
        # this_para = cv.node('paragraph')
        this_verse = cv.node('verse')
        # this_subverse = cv.node('subverse')
        
        # iterate through words and construct objects
        for word in text:

            wrdnum += 1

            data = word.split(' ')
            # word_data, lemmas = data[:7], data[7:]
            
            # segment out word data
            # bo_code, ref, brake, ketiv, qere, morph, strongs = word_data
            ref, part_of_speech, parsing_code, text, word, normalized_word, lemma = data

            morphology = ' '.join([part_of_speech, parsing_code])

            chapter = ref[2:4]
            verse = ref[4:]

            # strongs_lemma, anlex_lemma = ' '.join(lemmas).split('!') # reconstitute lemmas and split on !

            # chapt, verse, wrdnum = [int(v) for v in patts['section'].match(ref).groups()]

            # -- handle TF events --

            # # detect book boundary
            # if prev_book != book:

            #     # end subverse
            #     cv.feature(this_subverse, subverse=prev_subverse)
            #     cv.terminate(this_subverse)

            #     # end verse
            #     cv.feature(this_verse, verse=prev_verse)
            #     cv.terminate(this_verse)
                
            #     # end chapter
            #     cv.feature(this_chap, chapter=prev_chap)
            #     cv.terminate(this_chap)

            #     # end book
            #     cv.feature(this_book, book=book)
            #     cv.terminate(this_book)
                
            #     # new book, chapter, verse, and subverse begin
            #     this_book = cv.node('book')
            #     prev_book = book
            #     this_chap = cv.node('chapter')
            #     prev_chap = chapter
            #     this_verse = cv.node('verse')
            #     prev_verse = verse
            #     this_subverse = cv.node('subverse')
            #     prev_subverse = subverse
            #     wrdnum = 1
            
            # detect chapter boundary
            if prev_chap != chapter:

                # # end subverse
                # cv.feature(this_subverse, subverse=prev_subverse)
                # cv.terminate(this_subverse)
                
                # end verse
                cv.feature(this_verse, verse=prev_verse)
                cv.feature(this_verse, chapter=prev_chap)
                cv.feature(this_verse, book=book)
                cv.terminate(this_verse)
                
                # end chapter
                cv.feature(this_chap, chapter=prev_chap)
                cv.feature(this_verse, book=book)
                cv.terminate(this_chap)
                
                # new chapter, verse, and subverse begin
                this_chap = cv.node('chapter')
                prev_chap = chapter
                this_verse = cv.node('verse')
                prev_verse = verse
                # this_subverse = cv.node('subverse')
                # prev_subverse = subverse
                wrdnum = 1
            
            # detect verse boundary
            elif prev_verse != verse:

                # # end subverse
                # cv.feature(this_subverse, subverse=prev_subverse)
                # cv.terminate(this_subverse)

                # end verse
                cv.feature(this_verse, verse=prev_verse)
                cv.feature(this_verse, chapter=prev_chap)
                cv.feature(this_verse, book=book)
                cv.terminate(this_verse)

                # new verse and subverse begin
                this_verse = cv.node('verse')
                prev_verse = verse
                # this_subverse = cv.node('subverse')
                # prev_subverse = subverse
                wrdnum = 1

            # # detect subverse boundary
            # elif prev_subverse != subverse:
            #     cv.feature(this_subverse, subverse=prev_subverse)
            #     cv.terminate(this_subverse)
            #     this_subverse = cv.node('subverse')
            #     prev_subverse = subverse

                
            # detect paragraph boundary
            # if brake == 'P':
            #     cv.feature(this_para, para=para_track)
            #     cv.terminate(this_para)
            #     this_para = cv.node('paragraph') # start a new paragraph
            #     para_track += 1 # count paragraphs in the book

            if sentence_done:
                cv.feature(this_clause, clause=clause_track)
                cv.terminate(this_clause)
                cv.feature(this_sentence, sentence=sentence_track)
                cv.terminate(this_sentence)
                this_sentence = cv.node('sentence')
                sentence_track += 1
                this_clause = cv.node('clause')
                clause_track += 1

                sentence_done = False
                clause_done = False

            elif clause_done:
                cv.feature(this_clause, clause=clause_track)
                cv.terminate(this_clause)
                this_clause = cv.node('clause')
                clause_track += 1

                clause_done = False

            if text[-1:] == "." or text[-1:] == ";":
                sentence_done = True

            elif text[-1:] == "," or text[-1:] == "·":
                clause_done = True

                
                
            # make word object
            this_word = cv.slot()
            cv.feature(this_word, 
                       text=text,
                       word=word,
                    #    lex_utf8=lex_utf8,
                    #    g_cons_utf8=g_cons_utf8,
                    #    translit_SBL=translit_SBL,
                       morphology=morphology,
                       normalized_word=normalized_word,
                       lemma=lemma,
                       # ketiv=ketiv, 
                       # qere=qere, 
                       # strongs=strongs, 
                    #    str_lem=strongs_lemma.strip(),
                    #    anlex_lem=anlex_lemma.strip()
                      )
            cv.terminate(this_word)
        
        # end book and its objects
        # - end subverse
        # cv.feature(this_subverse, subverse=prev_subverse)
        # cv.terminate(this_subverse)

        # - end verse
        cv.feature(this_verse, verse=prev_verse)
        cv.feature(this_verse, chapter=prev_chap)
        cv.feature(this_verse, book=book)
        cv.terminate(this_verse)
        
        # - end paragraph
        # cv.feature(this_para, para=para_track)
        # cv.terminate(this_para)

        # - end clause
        cv.feature(this_clause, clause=clause_track)
        cv.terminate(this_clause)

        # - end sentence
        cv.feature(this_sentence, sentence=sentence_track)
        cv.terminate(this_sentence)
        
        # - end chapter
        cv.feature(this_chap, chapter=prev_chap)
        cv.feature(this_chap, book=book)
        cv.terminate(this_chap)
        
        # - end book
        cv.feature(this_book, book=book)
        cv.terminate(this_book)


slotType = 'word'
otext = {'fmt:text-orig-full':'{text} ',
         'sectionTypes':'book,chapter,verse',
         'sectionFeatures':'book,chapter,verse'}

generic = {'Name': 'MorphGNT:SBLGNT Greek New Testament',
           'Version': '6.12',
           'Author': 'James Tauber',
           'Editors': 'Adrian Negrea, Clacir Virmes, Oliver Glanz, Krysten Thomas',
           'Converter': 'Adrian Negrea', 
           'Source:':'https://github.com/morphgnt/sblgnt',
           'Note':'Feature descriptions adapted from sblgnt README'}

intFeatures = {'chapter', 'sentence', 'clause', 'verse'}

featureMeta = {'book': {'description': 'A book name'},
               'chapter': {'description': 'A chapter number'},
               'sentence': {'description': 'A sentence number'},
               'clause': {'description': 'A clause number'},
               'verse': {'description': 'A verse number'},
            #    'subverse': {'description': 'Subverse information'},
               'word': {'description': 'Word with punctuation stripped'},
            #    'lex_utf8': {'description': 'lex_utf8'},
            #    'g_cons_utf8': {'description': 'g_cons_utf8'},
            #    'translit_SBL': {'description': 'translit_SBL'},
               'morphology': {'description': 'morphology'},
               'text': {'description': 'Text as it appears in SBLGNT'},
               'normalized_word': {'description': 'Normalized word'},
               'lemma': {'description': 'Lemma'},
               # 'para': {'description': 'A paragraph number'},
               # 'ketiv': {'descrption': 'The text as it is written in the printed Tischendorf'},
               # 'qere': {'description': 'The text as the editor thinks it should have been'},
               # 'strongs': {'description': 'A word\'s number in Strongs'},
               # 'str_lem': {'description': 'Word lemma that corresponds to The NEW Strong\'sComplete Dictionary of Bible Words'},
               # 'anlex_lem': {'description': 'Word lemma that corresponds to Friberg, Friberg and Miller\'s ANLEX'}
              }


# configure metadata/output
version = '6.12'
generic['Version'] = version

output = os.path.join(output_dirs, version)

print(f'Processing Version {version}')
output_dir = output_dirs.format(version=version)

TF = Fabric(locations=output_dir, silent=True)
cv = CV(TF)

cv.walk(director,
                slotType,
                otext=otext,
                generic=generic,
                intFeatures=intFeatures,
                featureMeta=featureMeta,
                warn=True,
                force=False,)