import pandas as pd
from Bio.Blast import NCBIWWW, NCBIXML

def get_lenght(seq):
    return len(seq)


def gc_subsequence(seq):
    highest_subseq = ''
    highest_content = 0
    pos = 0
    for x in range(len(seq)-9):
        subseq = seq[x:x+10]
        gc_content = subseq.count('G') + subseq.count('C')
        if gc_content > highest_content:
            highest_content = gc_content
            highest_subseq = subseq
            pos = x
    if highest_content == 0:
        return 'This sequence has no G or C', 0, 0
    return highest_subseq, highest_content, pos



def read_fasta(text):
    sequences = {}
    current = ''
    for line in text.splitlines():
        if line == '':
            continue
        if line[0] == '>':
            current = line[1:]
            sequences[current] = ''
        else:
            sequences[current] += line
    return sequences


def read_csv(text):
    sequences = {}
    lines = text.strip().splitlines()[1:]
    for line in lines:
        info = line.split(',')
        sequences[info[0]] = info[1]
    return sequences
        


def get_nucleotides(seq):
    a = seq.count('A')
    t = seq.count('T')
    c = seq.count('C')
    g = seq.count('G')    
    total = a+t+c+g

    data = {0:['A', f'{a}bp', (a/total)*100], 1:['T', f'{t}bp', (t/total)*100], 2:['C',f'{c}bp', (c/total)*100], 3:['G', f'{g}bp', (g/total)*100]}
    df = pd.DataFrame.from_dict(data, orient='index', columns=['Base', 'Count', 'Percent'])
    return df




def biopython_search(seq):
    print('searching')
    result = NCBIWWW.qblast('blastn', 'nt', seq, format_type='Text')
    print('got it')
    # readable_result = result.read()
    # blast_record = NCBIXML.parse(readable_result)
    print(result)

if __name__ == '__main__':
    biopython_search('gctctgtcgcccaggctggagtgcagtggcgcgatctcgactcactgcaa')
