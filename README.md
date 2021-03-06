[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5807152.svg)](https://doi.org/10.5281/zenodo.5807152) [![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
# SBLGNT
This repository contains the SBL Greek New Testament (SBLGNT) in a TextFabric format. As a source for the CBLC version of SBLGNT we have used the version from MorphGNT as it is made available in their repository "sblgnt" (https://github.com/morphgnt/sblgnt). We have then converted the txt files into the TextFabric format (see https://github.com/CenterBLC/SBLGNT/tree/main/programs). This allows TF users to access the SBLGNT text in a convenient way and query it.

# Added Features
The CBLC version of the SBLGNT version has been enriched with several new features. We have split up the morphological coding into its proper own feature sets like person, number, gender, tense, part of speech, etc. In addition, we have created an alphabetic ordering of all lexemes. Also, word frequency information has been added. This helps instructors of Greek to develop vocab lists in alphabetic order for students. Also, we have added the Greek dictionary entry forms and English as found in the BibleOL (https://bibleol.3bmoodle.dk/). For licenses, please consult https://github.com/EzerIT/BibleOL. Finally, sentence divisions have been added. However, these divisions are simply based on the punctuation found in the Greek text. How the additional features we added were produced is documented in the feature production notebook (https://github.com/CenterBLC/NA/tree/main/programs)

# What’s next?
The CBLC version of the SBLGNT version is still a work in progress. On the morphological level, we plan to identify verbal and nominal classes (-ω verbs, -µι, a-declination, o-declination, etc.) and build additional feature sets for them. We plan to add syntax analysis and have been in contact with the opentext.org project on this matter. We are also planning to convert the syntax information produced by the Asian Bible Society and stored in the github organization “biblicalhumanities” (https://github.com/biblicalhumanities/greek-new-testament/tree/master/syntax-trees/sblgnt/xml).
# Why?
Text-Fabric has proven to be an excellent linguistic research tool as it can use richly annotated databases and integrates well into the python/pandas tools for data analysis. Since, except for the Tischendorf Text, Biblical Greek texts did not yet exist as TF apps, CBLC saw the need to make the Greek NT and the Greek text of the OT available as TF apps. In this way two different needs can be addressed:
1.	Linguistic Research into the Septuagint Greek and Koine Greek of the NT is made possible within the TF environment. Particularly valence analysis of Greek verbs will become possible. Also, valence comparison between Greek and Hebrew words can be carried out.
2.	Since the BibleOL uses the SBLGNT version, we now offer with the TF SBLGNT app the possibility to create vocab lists and identify text material for BibleOL based exercises.

# How to get started?
Run in a jupyter notebook the following command:
```phython
from tf.fabric import Fabric
from tf.app import use
NA = use("CenterBLC/SBLGNT", version="2022")
```
