from os import environ, makedirs
import os.path
import re
import sys
import gzip
import datetime

import requests
import bibtexparser


loca = "C:/tex/play.bib" # Custom location to append BibTeX entry


IGNORELIST = [
    "of", "and", "in", "at", "on", "the", "&",
    "für", "ab", "um"
]

MONTH_RE = re.compile("\s*month\s*=\s*\{\s*?(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s*\},?")
LATEST_ISSN = "http://www.issn.org/wp-content/uploads/2013/09/LTWA_20160915.txt"
ISSN_UPD = datetime.date(2016, 9, 15)

def unix_data_home():
    try:
        return environ['XDG_DATA_HOME']
    except KeyError:
        return os.path.join(environ['HOME'], '.local', 'share')


def windows_data_home():
    return environ['APPDATA']


def darwin_data_home():
    return os.path.join(environ['HOME'], 'Library', 'Application Support')


def data_home(folder=None):
    platform = sys.platform

    if platform == 'win32':
        data_dir = windows_data_home()
    elif platform == 'darwin':
        data_dir = darwin_data_home()
    else:
        data_dir = unix_data_home()

    if folder is None:
        return data_dir
    else:
        return os.path.join(data_dir, folder)


def dl_abbrev(fname='abbrev.txt.gz'):
    url = LATEST_ISSN
    r = requests.get(url, allow_redirects=True)
    data = r.content
    directory = data_home('citation')
    makedirs(directory)

    with gzip.open(os.path.join(directory, fname), 'wb') as f:
        f.write(data)


def load_abbrev(fname):
    """
    Loads the abbreviation database
    """
    # Check if we have the abbreviations list
    target = os.path.join(data_home('citation'), fname)

    if not os.path.isfile(target):
        print("%s not found; downloading..." % target, file=sys.stderr)
        dl_abbrev(fname)

    # Check for outdated abbreviation list
    mtime = datetime.date.fromtimestamp(os.path.getmtime(target))
    if not mtime > ISSN_UPD:
        print("%s is out of date; redownloading..." % target, file=sys.stderr)
        dl_abbrev(fname)

    # Load the abbreviations database into memory
    data = {}
    with gzip.open(target, 'rt', encoding="utf-16") as f:
        for line in f:
            # usually the first line starts with WORD
            if line.startswith('WORD'):
                continue
            parts = line.split("\t")
            langs = parts[2].split(", ")
            jname = parts[0]
            jabbrev = parts[1]
            data[jname.lower()] = jabbrev.lower()
    return data


def journal_abbrev(name):
    """
    Abbreviates a journal title
    """
    #data = load_abbrev(os.path.join(sys.path[0], "abbrev.txt.gz"))
    data = load_abbrev("abbrev.txt.gz")
    n_abbrev = []

    (name, _, _) = name.partition(":")
    parts = re.split("\s+", name)

    if len(parts) == 1 and len(parts[0]) < 12:
        return name
    for word in parts:
        # Do not abbreviate wordsin the IGNORELIST
        if word.lower() in IGNORELIST:
            continue
        for (k,v) in data.items():
            found = False

            # If the key ends with - it means we are checking for a prefix
            if k.endswith("-"):
                if word.lower().startswith(k[:-1]):
                    if v != "n.a.":
                        n_abbrev.append(v.capitalize())
                    else:
                        n_abbrev.append(word.lower().capitalize())
                    found = True
                    break
            # Else we are checking for a whole match
            else:
                if word.lower() == k:
                    if v != "n.a.":
                        n_abbrev.append(v.capitalize())
                    else:
                        n_abbrev.append(word.lower().capitalize())
                    found = True
                    break

        if not found:
            # If all characters are uppercase leave as is
            if not word.isupper():
                n_abbrev.append(word.capitalize())
            else:
                n_abbrev.append(word)
    return " ".join(n_abbrev)


def get_entry(doi):
    if doi[0:2] != "10":
        "It obviouly assumes that if it does not start with usual 10., it is arXiv code"
        url = 'https://dx.doi.org/10.48550/arXiv.%s' % doi
    else:    
        url = 'https://dx.doi.org/%s' % doi

    raw = requests.get(url, \
        headers={'Accept':'text/x-bibliography;style=bibtex'},
        timeout=2)
    if raw.ok and raw.status_code == 200:
        db = bibtexparser.loads(raw.content.decode('utf-8'))
        entry = db.entries[0]
        if 'journal' in entry.keys():
            jabbr = journal_abbrev(entry['journal'])
            if jabbr != entry['journal']:
                entry['shortjournal'] = jabbr
        if 'month' in entry.keys():
            month = entry['month'].lower()
            entry['month'] = month
        raw_result = bibtexparser.dumps(db).strip()
        lines = []
        for line in raw_result.splitlines():
            match = MONTH_RE.match(line)
            if match:
                if line.strip().endswith(","):
                    line = " month = %s," % match.group(1)
                else:
                    line = " month = %s" % match.group(1)
            lines.append(line)
        return "\n".join(lines)
    else:
        raise Exception("Could not get data for \"%s\" from CrossRef (status code)" %
                (url, raw.status_code))



if __name__ == "__main__":
    try:
        doi = sys.argv[1]
        aa = doi.split(",")
        print(aa)
        if aa[0] == "l":
            if len(aa) == 2:
                aa.pop(0)
                print(aa)
                data = get_entry(aa[0])
                print(data)
            elif len(aa) > 2:
                aa.pop(0)                
                for i in aa:
                    print(i)
                    data = get_entry(i)
                    print(data)
        elif len(doi.split(",")) == 1:
            print(doi)
            data = get_entry(doi)
            print(data)
            with open(loca, 'a', encoding="utf-8") as k:
                k.write(str(data))
                k.write(" \n")
        elif (len(doi.split(",")) > 1) & (doi[0:2] != "l,"):
            aa = doi.split(",")
            for i in aa:
                print(i)
                data = get_entry(i)
                print(data)
                with open(loca, 'a', encoding="utf-8") as k:
                    k.write(str(data))
                    k.write(" \n")
    except IndexError as ie:
        print("Usage: %s DOI" % os.path.basename(sys.argv[0]), file=sys.stderr)
        print("No DOI provided", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)