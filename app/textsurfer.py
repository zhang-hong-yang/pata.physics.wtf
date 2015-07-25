
from __future__ import print_function

from nltk.corpus import wordnet as wn
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import stopwords

from collections import defaultdict

import os

#############################################

# PROTOTYPE 01 - TEXT

#############################################

root_path = os.path.dirname(os.path.abspath(__file__))
root_path = root_path[:-4]
corpus_root = root_path + '/app/static/corpus'
book_list = PlaintextCorpusReader(corpus_root, '.*\.txt')  # root, fileid

############################################################
l_00 = book_list.words('00.faustroll.txt')
l_01 = book_list.words('01.poe1.txt')
l_02 = book_list.words('02.bergerac.txt')
l_03 = book_list.words('03.gospel.txt')
l_04 = book_list.words('04.bloy_french.txt')
l_05 = book_list.words('05.coleridge.txt')
l_06 = book_list.words('06.darien_french.txt')
l_07 = book_list.words('07.desbordes_french.txt')
l_08 = book_list.words('08.elskamp_french.txt')
l_09 = book_list.words('09.florian_french.txt')
l_10 = book_list.words('10.arabiannights.txt')
l_11 = book_list.words('11.grabbe_german.txt')
l_12 = book_list.words('12.kahn_french.txt')
l_13 = book_list.words('13.lautreamont_french.txt')
l_14 = book_list.words('14.maeterlinck.txt')
l_15 = book_list.words('15.mallarme_french.txt')
l_16 = book_list.words('16.mendes.txt')
l_17 = book_list.words('17.odyssey.txt')
l_18 = ''
l_19 = book_list.words('19.rabelais.txt')
l_20 = ''
l_21 = ''
l_22 = book_list.words('22.rimbaud_french.txt')
l_23 = book_list.words('23.schwob_german.txt')
l_24 = book_list.words('24.ubu_french.txt')
l_25 = book_list.words('25.verlaine.txt')
l_26 = book_list.words('26.verhaeren.txt')
l_27 = book_list.words('27.verne.txt')
############################################
en_stop = stopwords.words('english')
fr_stop = stopwords.words('french')
de_stop = stopwords.words('german')
############################################################

l_dict = defaultdict(list)

# l_dict structure:
# {word1: [[fileA, 0], [fileB, 0], ...],
#  word2: [[fileC, 0], [fileK, 0], ...],
#  ...
# }


def setupcorpus(nr, lang):
    for x, w in enumerate(nr):
        if w.isalpha() and (w.lower() not in lang):
            l_dict[w.lower()].append([nr.fileid[49:], x])

setupcorpus(l_00, en_stop), print('added 00')
setupcorpus(l_01, en_stop), print('added 01')
setupcorpus(l_02, en_stop), print('added 02')
setupcorpus(l_03, en_stop), print('added 03')
setupcorpus(l_04, fr_stop), print('added 04')
setupcorpus(l_05, en_stop), print('added 05')
setupcorpus(l_06, fr_stop), print('added 06')
setupcorpus(l_07, en_stop), print('added 07')
setupcorpus(l_08, fr_stop), print('added 08')
setupcorpus(l_09, fr_stop), print('added 09')
setupcorpus(l_10, en_stop), print('added 10')
setupcorpus(l_11, en_stop), print('added 11')
setupcorpus(l_12, fr_stop), print('added 12')
setupcorpus(l_13, fr_stop), print('added 13')
setupcorpus(l_14, en_stop), print('added 14')
setupcorpus(l_15, fr_stop), print('added 15')
setupcorpus(l_16, en_stop), print('added 16')
setupcorpus(l_17, en_stop), print('added 17')
setupcorpus(l_18, en_stop), print('added 18')
setupcorpus(l_19, en_stop), print('added 19')
setupcorpus(l_20, en_stop), print('added 20')
setupcorpus(l_21, en_stop), print('added 21')
setupcorpus(l_22, fr_stop), print('added 22')
setupcorpus(l_23, de_stop), print('added 23')
setupcorpus(l_24, fr_stop), print('added 24')
setupcorpus(l_25, en_stop), print('added 25')
setupcorpus(l_26, en_stop), print('added 26')
setupcorpus(l_27, en_stop), print('added 27')


def clinamen(w, i):
    total = 0
    sources = set()
    out = defaultdict(list)
    words = set([item for item in l_00
                if dameraulevenshtein(w, item) <= i])
    for r in words:
        files = set(sear(r))
        for e in files:
            sources.add(e)
            sent = pp_sent(r.lower(), e)
            if sent != []:
                total += 1
                out[r].append((get_title(e), sent))
    return out, words, sources, total


def syzygy(w):
    total = 0
    out = defaultdict(list)
    words = set()
    sources = set()
    wordsets = wn.synsets(w)  # returns a list of synsets
    for ws in wordsets:  # ws is a synset
        hypo = ws.hyponyms()  # returns a list of synsets
        if len(hypo) > 0:
            for h in hypo:  # h is a synset
                for l in h.lemmas():  # l is a lemma
                    # if str(l.name()) in froll_dict:
                    words.add(str(l.name()))
        hyper = ws.hypernyms()
        if len(hyper) > 0:
            for h in hyper:
                for l in h.lemmas():
                    # if str(l.name()) in froll_dict:
                    words.add(str(l.name()))
        holo = ws.member_holonyms()
        if len(holo) > 0:
            for h in holo:
                for l in h.lemmas():
                    # if str(l.name()) in froll_dict:
                    words.add(str(l.name()))
    for r in words:
        files = set(sear(r))
        for e in files:
            sources.add(e)
            sent = pp_sent(r.lower(), e)
            if sent != []:
                total += 1
                out[r].append((get_title(e), sent))
    return out, words, sources, total


def antinomy(w):
    total = 0
    out = defaultdict(list)
    words = set()
    sources = set()
    wordsets = wn.synsets(w)
    for ws in wordsets:
        anti = ws.lemmas()[0].antonyms()
        if len(anti) > 0:
            for a in anti:
                if str(a.name()) != w:
                    words.add(str(a.name()))
    for r in words:
        files = set(sear(r))
        for e in files:
            sources.add(e)
            sent = pp_sent(r.lower(), e)
            if sent != []:
                total += 1
                out[r].append((get_title(e), sent))
    return out, words, sources, total


def get_title(file):
    return {
        'l_00': 'Alfred Jarry: Exploits and Opinions of Dr. Faustroll, '
                'Pataphysician',
        'l_01': 'Edgar Allen Poe: Collected Works',
        'l_02': 'Cyrano de Bergerac: A Voyage to the Moon',
        'l_03': 'Saint Luke: The Gospel',
        'l_04': 'Leon Bloy: Le Desespere',
        'l_05': 'Samuel Taylor Coleridge: The Rime of the Ancient Mariner',
        'l_06': 'Georges Darien: Le Voleur',
        'l_07': 'Marceline Desbordes-Valmore: Le Livre des Meres et '
                'des Enfants',
        'l_08': 'Max Elskamp: Enluminures',
        'l_09': 'Jean-Pierre Claris de Florian: Les Deux Billets',
        'l_10': 'One Thousand and One Nights',
        'l_11': 'Christian Dietrich Grabbe: Scherz, Satire, Ironie und '
                'tiefere Bedeutung',
        'l_12': "Gustave Kahn: Le Conte de l'Or et Du Silence,",
        'l_13': 'Le Comte de Lautreamont: Les Chants de Maldoror',
        'l_14': 'Maurice Maeterlinck: Aglavaine and Selysette ',
        'l_15': 'Stephane Mallarme: Verse and Prose',
        'l_16': 'Mendes: The Mirror and la Divina Aventure',
        'l_17': 'Homer: The Odyssey',
        'l_18': 'Josephin Peladan: Babylon',
        'l_19': 'Francois Rabelais: Gargantua and Pantagruel',
        'l_20': "Jean de Chilra: L'Heure Sexuelle",
        'l_21': 'Henri de Regnier: La Canne de Jaspe',
        'l_22': 'Arthur Rimbaud: Poesies Completes',
        'l_23': 'Marcel Schwob: Der Kinderkreuzzug',
        'l_24': 'Alfred Jarry: Ubu Roi',
        'l_25': 'Paul Verlaine: Poems',
        'l_26': 'Emile Verhaeren: Poems',
        'l_27': 'Jules Verne: A Journey to the Centre of the Earth'
    }.get(file, 'Unknown')  # 'Unknown' is default if file not found


def sear(t):
    temp = []
    if l_dict.get(t.lower()):
        temp = l_dict.get(t.lower())
    temp1 = []
    for f in temp:
        x = ''.join(['l_', str((f[0])[0:2])])
        temp1.append(x)
    return temp1


def pp_sent(w, f):
    out = []
    ff = eval(f)
    pos = l_dict[w][0][1]
    pos_b = pos - 5
    pos_a = (pos + 1) + 5
    if pos_b >= 0 and pos_a <= len(ff):
        pre = ' '.join(ff[pos_b:pos])
        post = ' '.join(ff[pos+1:pos_a])
        # if pre != [] and post != []:
        out = (pre, post)
    return out


# http://mwh.geek.nz/2009/04/26/python-damerau-levenshtein-distance/
# MIT license.
def dameraulevenshtein(seq1, seq2):
    oneago = None
    thisrow = range(1, len(seq2) + 1) + [0]
    for x in xrange(len(seq1)):
        twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
        for y in xrange(len(seq2)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + (seq1[x] != seq2[y])
            thisrow[y] = min(delcost, addcost, subcost)
            if (x > 0 and y > 0 and seq1[x] == seq2[y - 1] and
               seq1[x - 1] == seq2[y] and seq1[x] != seq2[y]):
                    thisrow[y] = min(thisrow[y], twoago[y - 2] + 1)
    return thisrow[len(seq2) - 1]
