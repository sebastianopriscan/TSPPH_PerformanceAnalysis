import math as m

fileNames = ["ali535", "burma14", "gr96", "gr137", "gr202",
             "gr229", "gr431", "gr666", "ulysses16",
             "ulysses22"]

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
            entries.append(float(splline))
        coords.append(entries)

#    costMat = [0] * dimension * dimension

    output = open('formatted_instances/'+name+'.txt', mode='w')
    print(str(dimension), file=output)

    for j in range(0, dimension) :
        for q in range(0, dimension) :

            if j == q :
                print(str(0)+' ', file=output, end='')
#                costMat[j * dimension + q] = 0
                continue

            deg = nint(coords[j][1])
            min = coords[j][1] - deg
            latitude_j = m.pi * (deg + 5.0 * min / 3.0) / 180.0

            deg = nint(coords[j][2])
            min = coords[j][2] - deg
            longitude_j = m.pi * (deg + 5.0 * min / 3.0) / 180.0

            deg = nint(coords[q][1])
            min = coords[q][1] - deg
            latitude_q = m.pi * (deg + 5.0 * min / 3.0) / 180.0

            deg = nint(coords[q][2])
            min = coords[q][2] - deg
            longitude_q = m.pi * (deg + 5.0 * min / 3.0) / 180.0

            RRR = 6378.388

            q1 = m.cos(longitude_j - longitude_q)
            q2 = m.cos(latitude_j - latitude_q)
            q3 = m.cos(latitude_j + latitude_q)

#            costMat[j * dimension + q] = int( RRR * m.acos( 0.5*((1.0+q1)*q2 - (1.0-q1)*q3) ) + 1.0)
            cost = int( RRR * m.acos( 0.5*((1.0+q1)*q2 - (1.0-q1)*q3) ) + 1.0)
            print(str(cost)+' ', file=output, end='')
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