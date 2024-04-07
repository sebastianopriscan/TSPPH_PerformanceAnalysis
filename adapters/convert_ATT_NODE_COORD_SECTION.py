import math as m

fileNames = ["att48", "att532"]

def nint(x) :
    return int(x+0.5)
    
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

    for j in range(i, end) :
        line = lines[j].strip()
        splitted = line.split(" ")
        entries = []
        for splline in splitted :
            if splline == '' :
                continue
            entries.append(int(splline))
        coords.append(entries)

#    costMat = [0] * dimension * dimension

    output = open('formatted_instances/'+name+'.txt', mode='w')
    print(str(dimension), file=output)

    for j in range(0, dimension) :
        for q in range(0, dimension) :

            delta_x = coords[j][1] - coords[q][1]
            delta_y = coords[j][2] - coords[q][2]

            rij = m.sqrt((delta_x*delta_x + delta_y*delta_y) / 10.0)
            tij = nint(rij)

            if tij < rij :
                print(str(tij+1)+' ', file=output, end='')
#                costMat[j * dimension + q] = tij +1
            else :
                print(str(tij)+' ', file=output, end='')
#                costMat[j * dimension + q] = tij
        print('', file=output)

#    output = open('formatted_instances/'+name+'.txt', mode='w')
#
#    print(str(dimension), file=output)

#    for j in range(0, dimension) :
#        for q in range(0, dimension) :
#            print(str(costMat[j * dimension + q])+' ', file=output, end='')
#        print('', file=output)


def main() :
    for filename in fileNames :
        extendedPath = 'resources/' + filename + '.tsp'

        file = open(extendedPath, mode='r')

        convert(file)

if __name__ == '__main__' :
    main()