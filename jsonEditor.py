
class jsonFileTrack: 

    def __init__(self, name, path): 

        self.name = name
        self.path = path

        self.trajectoryCount = 0 

    def writeSat(self, name, timeStart, nPoints, timeSep, position, last_bool): 

        ch = ""

        ch += "{\n"

        ch += '\t\"nameSate\": \"%s\",\n'%name
        ch += '\t\"timeStart\": \"%s\",\n'%timeStart
        ch += '\t\"npoints\": \"%s\",\n'%nPoints
        ch += '\t\"timeSep\": \"%s\",\n'%timeSep
        ch += self.get_position(position)

        if last_bool == False: 
            ch += "},\n"
        else: 
            ch += "}\n"

        return ch

    def write(self, name_list, timeStart, nPoints, timeSep, position_list, N):

        with open(self.path, 'w') as f: 

            f.write('{\n')
            f.write('\"nameFile\": \"satellite_tle\",\n')
            f.write('\"satellites_infos\": [\n')

            for i in range(N): 
                
                if i < N-1: 
                    f.write(self.writeSat(name_list[i], timeStart, nPoints, timeSep, position_list[i], False))
                else: 
                    f.write(self.writeSat(name_list[i], timeStart, nPoints, timeSep, position_list[i], True))

            f.write(']\n')
            f.write('}')


    def get_position(self, position): 

        block = ""

        # open object
        block += '\t\"angularPosition\": [\n'

        for i in range(len(position)): 
            line_str = ('\t\t{\"longitude\": %s, \"latitude\": %s, \"height\": %s}'%(position[i][0], position[i][1], position[i][2]))
                
            block += line_str
            if i != len(position)-1:
                block += ',\n'
            else: 
                block += "\n"

        block += ']'

        return block