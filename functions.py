import pandas as pd


def get_lenght(seq):
    return len(seq)


def barplot():
    pass

def gc_subsequence(seq):
    highest_subseq = ''
    highest_content = 0
    for x in range(len(seq)-9):
        subseq = seq[x:x+10]
        gc_content = subseq.count('G') + subseq.count('C')
        if gc_content > highest_content:
            highest_content = gc_content
            highest_subseq = subseq
    if highest_content == 0:
        return 'This sequence has no G or C', 0
    return highest_subseq, highest_content


# print(gc_subsequence('AAAAGAGACCGCAGAAAAAGGAGGAAATTTTTAGGAGCC')) #7 'GAGACCGCAG'




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


text = '''
>Sequence_1
AGCTGCATCGATCGACGATCGATGACTAGCTGATCGATCGATCGATCGATCGAGCTACGATCGATGTACGATCGATCGATCGATCGACTGACTAGCTAGCTAGCATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGACGATCGATCGATCGATCGATCGATCGACTAGC
>Sequence_2
TTGTCAGTCGACTGCAATCACGACTCCGATCGATCGATCGATCGATGCTAGCTGATCGATCGATCGATCACGTACGACTAGACTAGCTACGACTAGT
ATACGATCGACATATCGTACGATCGCATGCTAGCTACGTAGCATCGTACCGATGCTAGCTAGCTACGTCAGT
>Sequence_3
AATCGCAGTAGCTGATCACATCGACTGATCTAGCATCGTAGCTACTACGATCTGATCGATCGATCGTGATCGATCGATCG
>Sequence_4
TACGATCATTTCGGCTATTCCGCTATACGTACGATCGCCCCCCCCCCCATCGACTGACTACGACTAGCTGAC
ACAGCTACTACGATTATACGATTCGTAGCTACGTACGATCGATCGATCGATGCTAGCTAGAC
TACTAGCTACGATCGATCGATCGATCGATCGATCAGCTACGATCGATCGATCGATCGATCAG
'''
# read_fasta(text)


def get_nucleotides(seq):
    a = seq.count('A')
    t = seq.count('T')
    c = seq.count('C')
    g = seq.count('G')    

    data = {0:['A', a], 1:['T', t], 2:['C',c], 3:['G', g]}
    df = pd.DataFrame.from_dict(data, orient='index', columns=['Base', 'Count'])
    return df


seq='TACGATCATTTCGGCTATTCCGCTATACGTACGATCGCCCCCCCCCCCATCGACTGACTACGACTAGCTGACACAGCTACTACGATTATACGATTCGTAGCTACGTACGATCGATCGATCGATGCTAGCTAGACTACTAGCTACGATCGATCGATCGATCGATCGATCAGCTACGATCGATCGATCGATCGATCAG'

# print(get_nucleotides(seq), len(seq))




# Function to handle based on if it is a fasta or csv file





