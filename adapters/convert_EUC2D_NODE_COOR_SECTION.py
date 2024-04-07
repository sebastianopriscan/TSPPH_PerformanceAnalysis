import math as m

fileNames = ["a280", "berlin52", "bier127", "ch130",
              "ch150", "d198", "d493", "d657", "d1291", "d1655",
              "d2103", "eil51", "eil76",
              "eil101", "fl417", "fl1400", "fl1577", "fl3795",
              "fnl4461", "gil262", "kroA100", "kroA150",
              "kroA200", "kroB100", "kroB150", "kroB200",
              "kroC100", "kroD100", "kroE100", "lin105",
              "lin318", "nrw1379", "p654", "pcb442", "pcb1173",
              "pcb3038", "pr76", "pr107", "pr124", "pr136",
              "pr144", "pr152", "pr226", "pr264", "pr299",
              "pr439", "pr1002", "pr2392", "rat99", "rat195",
              "rat575", "rat783", "rd100", "rd400", "rl1304",
              "rl1323", "rl1889", "rl5915", "rl5934",
              "st70", "ts225", "tsp225", "u159", "u574", "u724",
              "u1060", "u1432", "u1817", "u2152", "u2319",
              "vm1084", "vm1748"]

shadowed = ["brd14051", "d15112", "d18512", "rl11849", "usa13509"]

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
    
    while "NODE_COORD_SECTION" not in lines[i].strip() :
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

#   costMat = [0] * dimension * dimension

    output = open('formatted_instances/'+name+'.txt', mode='w')
    print(str(dimension), file=output)

    for j in range(0, dimension) :
        for q in range(0, dimension) :
            delta_x = coords[j][1] - coords[q][1]
            delta_y = coords[j][2] - coords[q][2]

#            costMat[j * dimension + q] = m.sqrt(delta_x*delta_x + delta_y*delta_y)
            cost = m.sqrt(delta_x*delta_x + delta_y*delta_y)
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