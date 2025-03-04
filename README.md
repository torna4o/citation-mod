Below is the exact copy of the original branch's Readme from foucault (https://github.com/foucault/)
What I modified is as follows: Normally the generated citation only comes as a prompt to the command panel.
With my modification, it appends to a file of your choosing (preferably a.bib file) in addition to the command panel
prompt. You can change the location of the corresponding file to append citation from "loca" variable in line 198.


March 3, 2024 UPDATE!!
=======================

Now when the user put an "l," right before the first DOI, as:

> python saver2.py l,10.XXXX

it does not store the bibtex entry into a file, just list the result in CMD prompt. It is possible to list multiple DOI at once like:

> python saver2.py l,10.XXXX,10.YYYY

Moreover, to expedite working with arXiv entries, you may just put the article specific code, starting with the first two number corresponding to the last two digits of the year,

> python saver2.py 10.48550/arXiv.2211.14683

and

> python saver2.py 2211.14683

yield the same result. 


Janury 6, 2024 UPDATE!!
=======================

The usual structure to retrieve BibTeX entry to a specified .bib text file was as follows in Windows 10:

> python citation-mod.py 10.XXXXX

where 10.XXXXX is "doi of interest". Now it is possible to get more than one entries in one line as
> python citation-mod.py 10.XXXXX,10.YYYYY

where 10.YYYYY is another doi.


Below is the exact copy of the original branch's Readme



citation
========

About
-----
**citation** is a dead simple Python script used to download readily formatted
citations for use in bibtex just by providing its Document Object Identifier
(DOI). Cut and paste the output into your `.bib` file and you are ready to go!

    $ citation 10.1007/bf00883088
    @article{Foti_1977,
     author = {Foti, G. and Rimini, E. and Vitali, G. and Bertolotti, M.},
     doi = {10.1007/bf00883088},
     issn = {1432-0630},
     journal = {Applied Physics},
     month = oct,
     number = {2},
     pages = {189–191},
     publisher = {Springer Nature},
     shortjournal = {Appl. Phys.},
     title = {Amorphous-polycrystal transition induced by laser pulse in self-ion implanted silicon},
     url = {http://dx.doi.org/10.1007/bf00883088},
     volume = {14},
     year = {1977}
    }


If you are using vim you can do that directly from your editor by using the
following command

    :r !citation 10.1007/bf00883088

and the bibtex entry will be appended into your current buffer.

Features
--------
* Download bibtex entries with just the DOI of the article.
* Automatically generate the abbreviated journal name into the `shortjournal`
  bibtex field. If you use `biblatex` you can use this field instead of the
  `journal` to create a more compact bibliography.
* Automatically strip curly braces from month specifications (`{jan}` → `jan`).
  Enclosing month abbreviations in curly braces is a LaTeX literal and should
  be avoided if you want your citations to be sorted correctly in a
  chronological order.

Caveats
-------
**citation** should work fairly well at least for most western languages. It is
completely untested with anything else than latin and greek alphabet, so
expect things to break. Although **citation** will probably get your citations
correct the first time there is always the chance of typos or invalid
characters. These errors are propagated from CrossRef and are very hard to
catch. However this should not happen very often. In my PhD I only had to edit
3 or 4 citations out of a 400+ references.

Dependencies
------------

 * Python ≥ 3.2
 * [Requests](https://github.com/requests/requests)
 * [BibtexParser](https://github.com/sciunto-org/python-bibtexparser)

