#CountAllHexamers V3
#Bastian Stark
#June 4, 2024
#Short script for counting all hexamers in a FASTA file.

nucleotides = ['A', 'T', 'G', 'C']

#list of "whitelisted" chromosomes. Adjust as needed. Items in list will be used for counts, anything not in list will be skipped.
whiteListed = ['>chr1', '>chr2', '>chr3', '>chr4', '>chr5', '>chr6', '>chr7', '>chr8', '>chr9', '>chr10', '>chr11',
               '>chr12', '>chr13', '>chr14', '>chr15', '>chr16', '>chr17', '>chr18', '>chr19', '>chr20', '>chr21',
               '>chr22', '>chrX', '>chrY']

#function for checking if a hexamer contains only As, T, Gs, and Cs. Hexamer will not be counted if it contains any other letters.
def checkNUCs(nucList, sequence, m):
    n = 0
    for char in sequence:
        if char in nucList:
            n += 1
    if n == m:
        return 0
    else:
        return 1

#function for adding input hexamer to hexamer count dictionary and/or increasing count
def countHexamers(currentChrom, sequenceCounts, m):
    n = 0
    hexamer = ''
    for i in range(m):
        hexamer = hexamer + 'N'
    while len(hexamer) == m:
        hexamer = currentChrom[n:n + m]
        if hexamer not in sequenceCounts:
            if len(hexamer) == m and checkNUCs(nucleotides, hexamer, m) == 0:
                sequenceCounts[hexamer] = 1
        elif hexamer in sequenceCounts:
            sequenceCounts[hexamer] += 1
        n += 1
    return sequenceCounts

filename = input('Enter file name: ')
m = int(input('Enter -mer size (ex: a hexamer would be 6): '))

infile = open(f"{filename}.txt")
outfile = open(f"{filename}_{m}mer_counts.txt", "w")
currentChromName = ''
currentChrom = ''
sequenceCounts = {}
lines = infile.readlines()
for line in lines:
    line = line.strip('\t')
    line = line.strip('\n')
    #at beginning of new chromosome, wipes previous chromosome info and changes name of chromosome to current one
    if line.startswith('>'):
        print(f'Concatenating {line}')
        currentChromName = line
        sequenceCounts = countHexamers(currentChrom, sequenceCounts, m)
        currentChrom = ''
    #concatenates lines for current chromosome
    elif line.startswith('>') == False and currentChromName in whiteListed:
        currentChrom = currentChrom + line
    #code for skipping over chromosomes not included in whitelisted chromosomes
    elif line.startswith('>') == False and currentChromName not in whiteListed:
        continue
    else:
        print('Error')
sequenceCounts = countHexamers(currentChrom, sequenceCounts, m)
for key in sequenceCounts:
    outfile.write(key + '\t' + str(sequenceCounts[key]) + '\n')