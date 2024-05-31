nucleotides = ['A', 'T', 'G', 'C']

whiteListed = ['>chr1', '>chr2', '>chr3', '>chr4', '>chr5', '>chr6', '>chr7', '>chr8', '>chr9', '>chr10', '>chr11',
               '>chr12', '>chr13', '>chr14', '>chr15', '>chr16', '>chr17', '>chr18', '>chr19', '>chr20', '>chr21',
               '>chr22', '>chrX', '>chrY']

def checkNUCs(nucList, sequence):
    n = 0
    for char in sequence:
        if char in nucList:
            n += 1
    if n == 6:
        return 0
    else:
        return 1

def countHexamers(currentChrom, sequenceCounts):
    n = 0
    hexamer = 'NNNNNN'
    while len(hexamer) == 6:
        hexamer = currentChrom[n:n + 6]
        if hexamer not in sequenceCounts:
            if len(hexamer) == 6 and checkNUCs(nucleotides, hexamer) == 0:
                sequenceCounts[hexamer] = 1
        elif hexamer in sequenceCounts:
            sequenceCounts[hexamer] += 1
        n += 1
    return sequenceCounts

filename = input('Enter file name: ')

infile = open(f"{filename}")
outfile = open(f"{filename}_counts.txt", "w")
currentChromName = ''
currentChrom = ''
sequenceCounts = {}
lines = infile.readlines()
for line in lines:
    line = line.strip('\t')
    line = line.strip('\n')
    if line.startswith('>'):
        print(f'Concatenating {line}')
        currentChromName = line
        sequenceCounts = countHexamers(currentChrom, sequenceCounts)
        currentChrom = ''
    elif line.startswith('>') == False and currentChromName in whiteListed:
        currentChrom = currentChrom + line
    elif line.startswith('>') == False and currentChromName not in whiteListed:
        continue
    else:
        print('Error')
sequenceCounts = countHexamers(currentChrom, sequenceCounts)
for key in sequenceCounts:
    outfile.write(key + '\t' + str(sequenceCounts[key]) + '\n')