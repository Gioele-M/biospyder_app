import pandas as pd
from Bio.Blast import NCBIWWW, NCBIXML

def get_lenght(seq):
    return len(seq)


#Get 10bp subsequence with highest GC content
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


#Read fasta file
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


#Read csv file
def read_csv(text):
    sequences = {}
    lines = text.strip().splitlines()[1:]
    for line in lines:
        info = line.split(',')
        sequences[info[0]] = info[1]
    return sequences
        

# Get DF with nucleotide count
def get_nucleotides(seq):
    a = seq.count('A')
    t = seq.count('T')
    c = seq.count('C')
    g = seq.count('G')    
    total = a+t+c+g

    data = {0:['A', f'{a}bp', (a/total)*100], 1:['T', f'{t}bp', (t/total)*100], 2:['C',f'{c}bp', (c/total)*100], 3:['G', f'{g}bp', (g/total)*100]}
    df = pd.DataFrame.from_dict(data, orient='index', columns=['Base', 'Count', 'Percent'])
    return df



# BLAST search function
# This function was not implemented because of the excessive runtime of the qblast function
def biopython_search(seq):
    result = NCBIWWW.qblast('blastn', 'nt', seq, format_type='Text')
    # readable_result = result.read()
    # blast_record = NCBIXML.parse(readable_result)
    print(result)

