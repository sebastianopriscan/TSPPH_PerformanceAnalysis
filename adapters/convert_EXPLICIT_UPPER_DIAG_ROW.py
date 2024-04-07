import math as m

filenames = ["si175", "si535", "si1032"]

def convert(file) :
    lines = file.readlines()

    name = ''
    dimension = 0
    i = 0
    while ":" in lines[i] :
        if "DIMENSION" in lines[i] :
            dimension = int(lines[i][lines[i].find(":")+1:].strip())

        if "NAME" in lines[i] :
            name = lines[i][lines[i].find(":")+1:].strip()

        if i < len(lines) :
            i += 1
        else :
            break
    
    i = i + 1
    end = dimension + i -1
    coords = []

    j = i
    line = lines[j].strip()

    while 'EOF' not in line and 'DISPLAY_DATA_SECTION' not in line :
        line = lines[j].strip()
        splitted = line.split(" ")
        entries = []
        for splline in splitted :
            if splline == '' :
                continue
            entries.append(int(splline))
        coords += entries
        j += 1
        line = lines[j].strip()

#    for j in range(i, end) :
#        line = lines[j].strip()
#        splitted = line.split(" ")
#        entries = []
#        for splline in splitted :
#            if splline == '' :
#                continue
#            entries.append(int(splline))
#        coords += entries

    costmat = [0] * dimension * dimension

    list_idx = 0
    for j in range(0, dimension) :
        for q in range(j, dimension) :
#            if j == q :
#                costmat[j * dimension + q] = 0
#                continue
            costmat[j * dimension + q] = coords[list_idx]
            costmat[q * dimension + j] = coords[list_idx]
            list_idx += 1

    output = open('formatted_instances/'+name+'.txt', mode='w')

    print(str(dimension), file=output)

    for j in range(0, dimension) :
        for q in range(0, dimension) :
            print(str(costmat[j * dimension + q])+' ', file=output, end='')
        print('', file=output)


def main() :
    for filename in filenames :
        extendedpath = 'resources/' + filename + '.tsp'

        file = open(extendedpath, mode='r')

        convert(file)

if __name__ == '__main__' :
    main()