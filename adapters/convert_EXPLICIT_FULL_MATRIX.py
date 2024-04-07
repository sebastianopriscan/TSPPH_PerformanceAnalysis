import math as m

filenames = ["bays29", "swiss42", "br17", "ft53", "ft70",
             "ftv33", "ftv35", "ftv38", "ftv44", "ftv47",
             "ftv55", "ftv64", "ftv70", "ftv170",
             "kro124p", "p43", "rbg323", "rbg358",
             "rbg403", "rbg443", "ry48p"]

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
    end = dimension + i
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

#    costmat = [0] * dimension * dimension

    output = open('formatted_instances/'+name+'.txt', mode='w')
    print(str(dimension), file=output)

    list_idx = 0
    for j in range(0, dimension) :
        for q in range(0, dimension) :
            if i == j :
                print(str(0)+' ', file=output, end='')
#                costmat[j * dimension + q] = 0
            else :
                print(str(coords[list_idx])+' ', file=output, end='')
#                costmat[j * dimension + q] = coords[list_idx]
            list_idx += 1
        print('', file=output)

#    output = open('formatted_instances/'+name+'.txt', mode='w')
#
#    print(str(dimension), file=output)

#    for j in range(0, dimension) :
#        for q in range(0, dimension) :
#            print(str(costmat[j * dimension + q])+' ', file=output, end='')
#        print('', file=output)


def main() :
    for filename in filenames :
        extendedpath = 'resources/' + filename + '.tsp'

        try :
            file = open(extendedpath, mode='r')
        except Exception :
            extendedpath = 'resources/' + filename + '.atsp'
            file = open(extendedpath, mode='r')

        convert(file)

if __name__ == '__main__' :
    main()