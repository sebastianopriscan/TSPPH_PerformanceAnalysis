import math as m

fileNames = ["dsj1000", "pla7397"]

shadowed = ["pla33810", "pla85900"]

def nint(x) :
    return int(x + 0.5)

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
            try :
                entries.append(int(splline))
            except Exception :
                entries.append(float(splline))

        coords.append(entries)

#    costMat = [0] * dimension * dimension
    output = open('formatted_instances/'+name+'.txt', mode='w')
    print(str(dimension), file=output)

    for j in range(0, dimension) :
        for q in range(0, dimension) :
            delta_x = coords[j][1] - coords[q][1]
            delta_y = coords[j][2] - coords[q][2]

#            costMat[j * dimension + q] = nint(m.sqrt(delta_x*delta_x + delta_y*delta_y))
            cost = nint(m.sqrt(delta_x*delta_x + delta_y*delta_y))
            print(str(cost)+' ', file=output, end='')
        print('', file=output)

#    output = open('formatted_instances/'+name+'.txt', mode='w')

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