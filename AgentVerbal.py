# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
#from PIL import Image

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an integer representing its
    # answer to the question: "1", "2", "3", "4", "5", or "6". These integers
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName() (as Strings).
    #
    # In addition to returning your answer at the end of the method, your Agent
    # may also call problem.checkAnswer(int givenAnswer). The parameter
    # passed to checkAnswer should be your Agent's current guess for the
    # problem; checkAnswer will return the correct answer to the problem. This
    # allows your Agent to check its answer. Note, however, that after your
    # agent has called checkAnswer, it will *not* be able to change its answer.
    # checkAnswer is used to allow your Agent to learn from its incorrect
    # answers; however, your Agent cannot change the answer to a question it
    # has already answered.
    #
    # If your Agent calls checkAnswer during execution of Solve, the answer it
    # returns will be ignored; otherwise, the answer returned at the end of
    # Solve will be taken as your Agent's answer to this problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.


    #map objects in fig A to B
    def map(self,A,B):

        # map each object in figure A to an object in figure B
        objsA = A.objects
        objsB = B.objects
        mapping = {}
        relations=["inside","above","overlaps","left-of"]
        sizes = {"very small":0,"small":1,"medium":2,"large":3,"very large":4,"huge":5}
        transform = {}
        diffattr = {} #store which attributes are different between 2 objects
        weight = 0

        for Akey in objsA:
            objA = objsA[Akey]
            diffattr[Akey]={}

            for Bkey in objsB:

                diff = 0
                objB = objsB[Bkey]
                diffattr[Akey][Bkey]=[]
                for key in objA.attributes.keys():
                    if key in objB.attributes.keys() and objA.attributes[key]!=objB.attributes[key]:
                        if key not in relations:
                            diff+=1
                            diffattr[Akey][Bkey].append(key)
                        else:
                            if len(objsA)==len(objsB):#only check relations if no objects are
                            # being added or deleted
                                relationlistA = objA.attributes[key].split(",")
                                relationlistB = objB.attributes[key].split(",")
                                if len(relationlistA)!=len(relationlistB):
                                    diff+=1


                #if all the attributes are same and the object does not have a mapping already
                #then add to mapping
                if diff == 0 and Akey not in mapping.keys() and Bkey not in mapping.values():
                    mapping[Akey] = Bkey
                    transform[Akey]={}
                    transform[Akey][Bkey]=["unchanged"]
                    weight += 30

        lefttomapA = [key for key in objsA if key not in mapping.keys()]
        lefttomapB = [key for key in  objsB if key not in mapping.values()]

        for Akey in lefttomapA:
            for Bkey in lefttomapB:
                objA = objsA[Akey]
                objB = objsB[Bkey]
                atta = objA.attributes
                attb = objB.attributes
                transform[Akey]={}
                transform[Akey][Bkey]=[]
                
                if atta["shape"]==attb["shape"]:
                    # add weights to the transformation
                    if "width" in diffattr[Akey][Bkey]:
                        sizechange = sizes[attb["width"]]-sizes[atta["width"]]
                        transform[Akey][Bkey].append("width:"+str(sizechange))
                        weight+=4

                    if "height" in diffattr[Akey][Bkey]:
                        sizechange = sizes[attb["height"]]-sizes[atta["height"]]
                        transform[Akey][Bkey].append("height:"+str(sizechange))
                        weight+=4

                    if "size" in diffattr[Akey][Bkey]:
                        
                        sizechange = sizes[attb["size"]]-sizes[atta["size"]]
                        transform[Akey][Bkey].append("size:"+str(sizechange))
                        weight+=4
                    
                    if "fill" in diffattr[Akey][Bkey]:
                        transform[Akey][Bkey].append("fill "+attb["fill"])
                        weight+=10

                    if "angle" in diffattr[Akey][Bkey]:
                    #check for reflection cases
                        angleA = int(atta["angle"])
                        angleB = int(attb["angle"])
                        # first and second quadrants
                        if angleA >=0 and angleA <=180:
                            if angleB == 180 - angleA:
                                transform[Akey][Bkey].append("reflectedY")
                                weight+=10
                            elif angleB == 360 - angleA:
                                transform[Akey][Bkey].append("reflectedY")
                                weight+=10
                            else:
                                angle=1
                        # third and fourth quadrant
                        elif angleA >180 and angleA <= 360:
                            if angleB == 540 - angleA:
                                transform[Akey][Bkey].append("reflectedY")
                                weight+=10
                            elif angleB == 360 - angleA:
                                transform[Akey][Bkey].append("reflectedX")
                                weight+=10
                            else:
                                transform[Akey][Bkey].append("rotated "+str(int(attb["angle"])-int(atta["angle"])))
                                weight+=8


                    if "alignment" in atta.keys() and "alignment" in attb.keys():
                        alignA = atta["alignment"].split("-")

                        alignB = attb["alignment"].split("-")
                        
                        if alignA[0]!=alignB[0]:
                            # alignment change about Y-axis
                            transform[Akey][Bkey].append("alignedY")
                            weight+=6
                        if alignA[1]!=alignB[1]:
                            # alignment change about X-axis
                            transform[Akey][Bkey].append("alignedX")
                            weight+=6

                    if Akey not in mapping.keys() and Bkey not in mapping.values():
                        mapping[Akey] = Bkey

        #deleted objects
        deleted = [key for key in objsA if key not in mapping.keys()]
        #added objects
        added = [key for key in  objsB if key not in mapping.values()]

        print A.name,"to",B.name
        print "mapping:",mapping
        print "transform:",transform
        print "added:",added
        print "deleted:",deleted
        print "weight:",weight
        #list of various dictionaries and lists and weight to return
        stufftoreturn = [mapping,transform,added,deleted,weight]
        return stufftoreturn

    def compare(self,collAB,collCD,A,B,C,D):
        transformAB = collAB[1]
        transformCD = collCD[1]
        objsA = A.objects
        objsB = B.objects
        objsC = C.objects
        objsD = D.objects
        mappingAB = collAB[0]
        mappingCD = collCD[0]
        relations=["inside","above","overlaps","left-of"]
        score=0

        listAB = []
        for Akey in transformAB:
            for Bkey in transformAB[Akey]:
                listAB.append(transformAB[Akey][Bkey])
        listCD = []
        for Ckey in transformCD:
            for Dkey in transformCD[Ckey]:
                listCD.append(transformCD[Ckey][Dkey])
        print "listAB:",listAB
        print "listCD:",listCD
        listAB.sort()
        listCD.sort()
        diffcount=0
        if len(listAB)==len(listCD):

            for i in range(0,len(listAB)):
                if listAB[i]==listCD[i]:
                    score+=20
                else:
                    diffcount+=1
                    storeattr = listAB[i]

        if diffcount==1:
            
            for Akey in transformAB:
                for Bkey in transformAB[Akey]:
                    if transformAB[Akey][Bkey]==storeattr:
                        
                        for Ckey in transformCD:
                            for Dkey in transformCD[Ckey]:
                                statr="".join(storeattr)
                                if statr in objsD[Dkey].attributes.keys() and statr in objsC[Ckey].attributes.keys() and objsD[Dkey].attributes[statr]==objsC[Ckey].attributes[statr]:
                                    score+=10

        addedAB = collAB[2]
        addedCD = collCD[2]
        deletedAB = collAB[3]
        deletedCD = collCD[3]

        lenA = len(objsA)
        lenB = len(objsB)
        lenC = len(objsC)
        lenD = len(objsD)
        lenaddAB = len(addedAB)
        lenaddCD = len(addedCD)
        lendelAB = len(deletedAB)
        lendelCD = len(deletedCD)

        if lenD != (lenC + lenaddAB - lendelAB):
            score-=50

        if len(addedAB)==len(addedCD):
            for objB in addedAB:
                for objD in addedCD:
                    for attr in objsB[objB].attributes:
                        
                        if attr in objsD[objD].attributes and attr not in relations:
                            
                            if objsB[objB].attributes[attr]!=objsD[objD].attributes[attr]:
                                print 
                                break
                            score+=20
        else:
            score-=20
            
        if len(deletedAB)==len(deletedCD):
            for objA in deletedAB:
                for objC in deletedCD:
                    for attr in objsA[objA].attributes:
                        if attr in objsC[objC].attributes:
                            if objsA[objA].attributes[attr]!=objsC[objC].attributes[attr]:

                                break
                            score+=20

        else:
            score-=20
        """this function should return a score integer for every comparison
         so, for every transformation that matches increase the score, and
         the one with the highest score wins"""

        print "Score:",score
        return score

    def Solve(self,problem):
        """for figure in problem.figures:
            for objects in problem.figures[figure].objects:
                for attr in problem.figures[figure].objects[objects].attributes:
                    print attr,":",problem.figures[figure].objects[objects].attributes[attr]"""
        figures = problem.figures;
        
        if problem.problemType == "2x2" and problem.hasVerbal == True:
            print "\n"+problem.name+"-------------------------------------------------------------------------"
            collH = []
            collH = Agent.map(self,figures["A"],figures["B"])
            mappingh = collH[0]
            transformh = collH[1]
            addedh = collH[2]
            deletedh = collH[3]
            weighth = collH[4]
            collV = []
            collV = Agent.map(self,figures["A"],figures["C"])
            mappingv = collV[0]
            transformv = collV[1]
            addedv  =collH[2]
            deletedv = collH[3]
            weightv = collV[4]

            if weighth>=weightv:
                print "Horizontal executes"
                ob = []
                ob.append(None)
                coll=[]
                coll.append(None)
                score=[]
                score.append(None)
                for i in range(1,7):
                    ob.append(figures[str(i)])
                    # print ob[i].name
                    coll.append(Agent.map(self,figures["C"],ob[i]))
                    score.append(Agent.compare(self,collH,coll[i],figures["A"],figures["B"],figures["C"],ob[i]))

                """check if the highest score passes the threshold value otherwise skip"""
                threshold = 10 #decide some value
                highest = max(score)
                if highest >= threshold:
                    for i in range(1,7):
                        if highest==score[i]:
                            print "Answer:",i
                            print "Correct:",problem.checkAnswer(i)
                            return i

            else:
                print "Vertical executes"
                ob = []
                ob.append(None)
                coll=[]
                coll.append(None)
                score=[]
                score.append(None)
                for i in range(1,7):
                    ob.append(figures[str(i)])
                    coll.append(Agent.map(self,figures["B"],ob[i]))
                    score.append(Agent.compare(self,collV,coll[i],figures["A"],figures["C"],figures["B"],ob[i]))

                """check if the highest score passes the threshold value otherwise skip"""
                threshold = 10 #decide some value
                highest = max(score)
                if highest >= threshold:
                    for i in range(1,7):
                        if highest==score[i]:
                            print "Answer:",i
                            print "Correct:",problem.checkAnswer(i)
                            return i
            
        elif problem.problemType == "3x3" and problem.hasVerbal == True:

            print "\n"+problem.name+"-------------------------------------------------------------------------"

            collAE = []
            collAE = Agent.map(self,figures["A"],figures["E"])
            mappingAE = collAE[0]
            transformAE = collAE[1]
            addedAE = collAE[2]
            deletedAE = collAE[3]
            weightAE = collAE[4]

            collGH = []
            collGH = Agent.map(self,figures["G"],figures["H"])
            mappingGH = collGH[0]
            transformGH = collGH[1]
            addedGH = collGH[2]
            deletedGH = collGH[3]
            weightGH = collGH[4]

            collCF = []
            collCF = Agent.map(self,figures["C"],figures["F"])
            mappingCF = collCF[0]
            transformCF = collCF[1]
            addedCF = collCF[2]
            deletedCF = collCF[3]
            weightCF = collCF[4]

            if weightAE>=weightGH and weightAE>=weightCF:
                print "Diagonal executes"
                ob = []
                ob.append(None)
                coll=[]
                coll.append(None)
                score=[]
                score.append(None)
                for i in range(1,9):
                    ob.append(figures[str(i)])
                    coll.append(Agent.map(self,figures["E"],ob[i]))
                    score.append(Agent.compare(self,collAE,coll[i],figures["A"],figures["E"],figures["E"],ob[i]))

                """check if the highest score passes the threshold value otherwise skip"""
                threshold = 10 
                highest = -1

                for i in range(1,9):
                    if score[i] >= highest:
                        highest = score[i]

                if highest >= threshold:
                    for i in xrange(8,0,-1):
                        if highest==score[i]:
                            
                            print "Answer:",i
                            #print "Correct:",problem.checkAnswer(i)
                            return i
    
            elif weightGH>=weightCF:
                print "Horizontal executes"
                ob = []
                ob.append(None)
                coll=[]
                coll.append(None)
                score=[]
                score.append(None)
                for i in range(1,9):
                    ob.append(figures[str(i)])
                    coll.append(Agent.map(self,figures["H"],ob[i]))
                    score.append(Agent.compare(self,collGH,coll[i],figures["G"],figures["H"],figures["H"],ob[i]))

                """check if the highest score passes the threshold value otherwise skip"""
                threshold = 10 
                highest = -1

                for i in range(1,9):
                    if score[i] >= highest:
                        highest = score[i]

                if highest >= threshold:
                    for i in xrange(8,0,-1):
                        if highest==score[i]:
                            
                            print "Answer:",i
                            #print "Correct:",problem.checkAnswer(i)
                            return i
            else:
                print "Vertical executes"
                ob = []
                ob.append(None)
                coll=[]
                coll.append(None)
                score=[]
                score.append(None)
                for i in range(1,9):
                    ob.append(figures[str(i)])
                    coll.append(Agent.map(self,figures["F"],ob[i]))
                    score.append(Agent.compare(self,collCF,coll[i],figures["C"],figures["F"],figures["F"],ob[i]))

                """check if the highest score passes the threshold value otherwise skip"""
                threshold = 10 
                highest = -1

                for i in range(1,9):
                    if score[i] >= highest:
                        highest = score[i]

                if highest >= threshold:
                    for i in xrange(8,0,-1):
                        if highest==score[i]:
                            
                            print "Answer:",i
                            #print "Correct:",problem.checkAnswer(i)
                            return i

        return -1