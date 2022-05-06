# Quick script to take one CSV and check if a selected column exists in another CSV
# Last updated 5/5/2022 MTG 

# Get necessary libraries
import csv  # https://docs.python.org/3/library/csv.html

# Variables needed
csvSource = 'source.csv'  # What we are going to look for (Source CSV); Expected to have a header row
csvSColumn = 1  # Column for match in Source CSV
csvDest = 'dest.csv'  # Where we are going to look for it (Destination CSV); Expected to have a header row
csvDColumn = 0  # Column for match in Destination CSV
outFile = 'outfile.csv'  # Output list of found matches; Will not have a header row


def checkFiles():
    '''
    This function checks our files that we need and system permissions, etc.
    '''
    try:
        with open(csvSource, 'r') as t1, open(csvDest, 'r') as t2, open(outFile, 'w') as t3:
            return True
    except IOError:
        return False

def csvSourceWork():
	'''
	This function does the CSV Source work.
	'''
	csvSList = []
	with open(csvSource, 'r') as f1:
	    reader1 = csv.reader(f1, delimiter=',')
	    next(reader1, None)  # Skip row header
	    for sLine in reader1:
		    csvSList.append(sLine[csvSColumn])
	return csvSList

def csvDestWork():
    '''
    This function does the CSV Destination work.
    '''
    csvDList = []
    with open(csvDest, 'r') as f2:
        reader2 = csv.reader(f2, delimiter=',')
        next(reader2, None)  # Skip row header
        for dLine in reader2:
            csvDList.append(dLine[csvDColumn])
    return csvDList

def csvMatch(sListF, dListF):
    '''
    This function writes out CSV matches.
    '''
    countFound1 = 0
    with open(outFile, 'w', newline='') as f3:
        for i in sListF:
            if i in dListF:
                f3.write(i+'\n')
                countFound1 = countFound1+1
    return countFound1

def csvMod(sListF):
    '''
    This function lets you modify the Source CSV if you so choose.
    '''
    countFound2 = 0
    with open(csvDest, 'r') as f4, open(outFile, 'w', newline='') as f5:
        reader3 = csv.reader(f4, delimiter=',')
        next(reader3, None)  # Skip row header
        writer1 = csv.writer(f5)
        for mLine in reader3:
            if mLine[csvDColumn] in sListF:
                mLine.append('MATCH')
                writer1.writerow(mLine)
                countFound2 = countFound2+1
            else:
                writer1.writerow(mLine)
    return countFound2


if __name__ == '__main__':
    filesExist = checkFiles()
    if filesExist == True:
        pass
    else:
        sys.exit('Check the input files, permissions, etc!')
    sListF = csvSourceWork()
    dListF = csvDestWork()
    ### csvOut = csvMatch(sListF, dListF)  # Use this one to write out matches.
    ### csvOut = csvMod(sListF)  # Use this one to write out a mod of the source CSV.
    try:
        print('Found '+str(csvOut)+' match(es)! Check the output file.')
    except:
        print('Uncomment one of the \'csvOut\' functions!')