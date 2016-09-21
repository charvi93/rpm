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
from PIL import Image

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


    def transform3(self,A,B,C,D,E,F,G,H):
        Aload = A.load()
        Bload = B.load()
        Cload = C.load()
        Dload = D.load()
        Eload = E.load()
        Fload = F.load()
        Gload = G.load()
        Hload = H.load()
        blackAupper = 0
        blackAlower = 0
        blackBupper = 0
        blackBlower = 0
        blackCupper = 0
        blackClower = 0
        blackA = 0
        blackB = 0
        blackC = 0
        blackD = 0
        blackE = 0
        blackF = 0
        blackG = 0
        blackH = 0
        intersection = 0
        intersectionV = 0
        common = 0
        transform = ""
        for i in range(0, A.size[0]):
            for j in range(0, A.size[1]):
                pixelA = Aload[i, j]
                pixelB = Bload[i, j]
                pixelC = Cload[i,j]
                pixelD = Dload[i, j]
                pixelE = Eload[i, j]
                pixelF = Fload[i,j]
                pixelG = Gload[i, j]
                pixelH = Hload[i, j]

                if pixelA == 0:
                    blackA +=1
                    if j <A.size[0]/2:
                        blackAupper+=1
                    else:
                        blackAlower += 1


                if pixelB == 0:
                    blackB+= 1
                    if j <A.size[0]/2:
                        blackBupper+=1
                    else:
                        blackBlower += 1
                if pixelC == 0:
                    blackC += 1
                    if j <A.size[0]/2:
                        blackCupper+=1
                    else:
                        blackClower += 1
                if pixelD == 0:
                    blackD += 1
                if pixelE == 0:
                    blackE += 1
                if pixelF == 0:
                    blackF += 1
                if pixelG == 0:
                    blackG += 1
                if pixelH == 0:
                    blackH += 1
                if pixelA == 0 and pixelB == 0:
                    intersection += 1
                if pixelA == 0 and pixelD == 0:
                    intersectionV += 1
                if pixelA == pixelB == pixelC == pixelD == pixelE == pixelF == pixelG == pixelH == 0:
                    common += 1
        
        offset = 105
        #if blackA + blackB in range(blackC - offset,blackC+offset):
        #    transform = "A+B"
        #print "intersection: ", intersection
        #print "blackC: ", blackC
        if blackA in range(blackB-offset,blackB + offset) and blackC in range(blackB-offset,blackB + offset):
            transform = "same"
        elif blackC in range(blackB - blackA - offset - intersection,blackB - blackA + offset - intersection):
            transform = "B-A"
        elif blackC in range(blackB - blackA - offset - (2*intersection),blackB - blackA + offset - (2*intersection)):
            transform = "B-A-intersection"

        elif blackC in range(blackA - blackB - offset,blackA - blackB + offset):
            transform = "A-B"
        
        elif blackC in range(blackA + blackB - intersection - offset,blackA+blackB-intersection+offset):
            transform = "A+B"
        
        elif blackC in range(blackA + blackB +common- (2*intersection)  -(2*offset),blackA+blackB+common-(2*intersection)-offset+12):
            transform = "A+B-intersection+common"
        elif blackC in range(blackA + blackB - (2*intersection) - offset,blackA+blackB-(2*intersection)+offset):
            transform = "A+B-intersection"
        elif blackC in range(intersection-offset,intersection+offset):
            transform = "intersection"
        elif blackA+blackB+blackC in range(blackD+blackE+blackF - offset,blackD+blackE+blackF+offset):
            transform = "sum horizontal"
        elif blackA+blackD+blackG in range(blackB + blackE + blackH - offset, blackB+blackE+blackH+offset):
            transform = "sum vertical"
        elif abs(blackD-blackA) in range(abs(blackE-blackB)-offset,abs(blackE - blackB) + offset) and abs(blackF-blackC) in range(abs(blackE-blackB)-offset,abs(blackE - blackB) + offset):
            transform = "same diff vertical"
        elif abs(blackB - blackA) in range (abs(blackE - blackD) - offset,abs(blackE - blackD) + offset) and abs(blackH - blackG) in range (abs(blackE - blackD) - offset,abs(blackE - blackD) + offset):
            transform = "same diff horizontal"
        elif blackCupper in range(blackAupper - offset, blackAupper+offset) and blackClower in range(blackBlower - offset,blackBlower+offset):
            transform = "upper A lower B"
        elif blackClower in range(blackAupper - offset, blackAupper+offset) and blackCupper in range(blackBlower - offset,blackBlower+offset):
            transform = "lower A upper B"
        elif blackC in range(2*blackB - offset,2*blackB + offset) and blackB in range(2*blackA - offset,2*blackA+offset):
            transform = "double horizontal"
        elif blackG in range(2*blackD - offset,2*blackD + offset) and blackD in range(2*blackA - offset,2*blackA+offset):
            transform = "double vertical"
        elif blackG in range(blackA + blackD - (2*intersectionV) - offset,blackA + blackD - (2*intersectionV) + offset):
            transform = "A+D-intersection"

        if transform == "A+B" and intersection in range (200,205):
            transform = "A+B-intersection"
        
        return transform

    #the below method was to be used for blob detection but it's not completely accurate in detecting objects
    def blob(self,A):
        objects = {}
        Aload = A.load()
        maxcount = 5
        objno  =1
        black = 1
        while black == 1 and maxcount > 0:
            maxcount -= 1
            tagged = []
            whitecount = 0
            for i in range(0, A.size[0]):
                for j in range(0, A.size[1]):
                    pixelA = Aload[i, j]
                    if Aload[i,j] == 0 and len(tagged) == 0:
                        tagged.append([i,j])
                        print tagged
                        Aload[i,j]=255
                    if Aload[i,j] == 0 and ([i+1,j] in tagged or [i,j+1] in tagged or [i-1,j] in tagged or [i,j-1] in tagged or [i+1,j+1] in tagged or [i+1,j-1] in tagged or [i-1,j+1] in tagged or [i-1,j-1] in tagged or [i-1,j-2] in tagged or [i-1,j+2] in tagged or [i+1,j-2] in tagged or [i+1,j+2] in tagged or [i+2,j-1] in tagged or [i-2,j-1] in tagged or [i+2,j+1] in tagged or [i-2,j+1] in tagged):
                        tagged.append([i,j])
                        Aload[i,j]=255
                    if Aload[i,j] == 255:
                        whitecount+=1
            if len(tagged)>0:
                objects[objno]=tagged
                objno += 1
            if whitecount == A.size[0]*A.size[1]:
                black = 0

        return objno-1



    def transform(self,A,B):
        

        Aload = A.load()
        Bload = B.load()
        same=0 
        blackA = 0
        blackB = 0
        offset = 110
        transform = ""
        for i in range(0, A.size[0]):
            for j in range(0, A.size[1]):
                pixelA = Aload[i, j]
                pixelB = Bload[i, j]
                if pixelA == 0:
                    blackA += 1
                if pixelB == 0:
                    blackB += 1
                if pixelA == 0 and pixelB ==0:
                    same+=1

        if blackB in range(blackA - offset,blackA + offset):
            transform = "same"
        return transform


        
    def Solve(self,problem):
        
        if problem.problemType == "3x3" and problem.hasVisual:
            figures = problem.figures
            A = Image.open(figures["A"].visualFilename)
            B = Image.open(figures["B"].visualFilename)
            C = Image.open(figures["C"].visualFilename)
            D = Image.open(figures["D"].visualFilename)
            E = Image.open(figures["E"].visualFilename)
            F = Image.open(figures["F"].visualFilename)
            G = Image.open(figures["G"].visualFilename)
            H = Image.open(figures["H"].visualFilename)
            o1 = Image.open(figures["1"].visualFilename)
            o2 = Image.open(figures["2"].visualFilename)
            o3 = Image.open(figures["3"].visualFilename)
            o4 = Image.open(figures["4"].visualFilename)
            o5 = Image.open(figures["5"].visualFilename)
            o6 = Image.open(figures["6"].visualFilename)
            o7 = Image.open(figures["7"].visualFilename)
            o8 = Image.open(figures["8"].visualFilename)
            A = A.convert("L")
            B = B.convert("L")
            C = C.convert("L")
            D = D.convert("L")
            E = E.convert("L")
            F = F.convert("L")
            G = G.convert("L")
            H = H.convert("L")
            o1 = o1.convert("L")
            o2 = o2.convert("L")
            o3 = o3.convert("L")
            o4 = o4.convert("L")
            o5 = o5.convert("L")
            o6 = o6.convert("L")
            o7 = o7.convert("L")
            o8 = o8.convert("L")
            print "\n"
            print problem.name+"---------------------------------------"
            #diffimg = self.transform(G,H)
            #ans = self.answer(H,diffimg)
            transformABC = self.transform3(A,B,C,D,E,F,G,H)
            transform1 = self.transform3(G,H,o1,D,E,F,A,B)
            transform2 = self.transform3(G,H,o2,D,E,F,A,B)
            transform3 = self.transform3(G,H,o3,D,E,F,A,B)
            transform4 = self.transform3(G,H,o4,D,E,F,A,B)
            transform5 = self.transform3(G,H,o5,D,E,F,A,B)
            transform6 = self.transform3(G,H,o6,D,E,F,A,B)
            transform7 = self.transform3(G,H,o7,D,E,F,A,B)
            transform8 = self.transform3(G,H,o8,D,E,F,A,B)
            
            #self.blob(A)
            print "transformation:",transformABC

            if transformABC != "":
                if transformABC == transform1:
                    return 1
                elif transformABC == transform2:
                    return 2
                elif transformABC == transform3:
                    return 3
                elif transformABC == transform4:
                    return 4
                elif transformABC == transform5:
                    return 5
                elif transformABC == transform6:
                    return 6
                elif transformABC == transform7:
                    return 7
                elif transformABC == transform8:
                    return 8


            transformABC = self.transform(A,E)
            transform1 = self.transform(E,o1)
            transform2 = self.transform(E,o2)
            transform3 = self.transform(E,o3)
            transform4 = self.transform(E,o4)
            transform5 = self.transform(E,o5)
            transform6 = self.transform(E,o6)
            transform7 = self.transform(E,o7)
            transform8 = self.transform(E,o8)
            print "Diagonal --------------------" 
            print "AE:",transformABC

            if transformABC != "":
                if transformABC == transform1:
                    return 1
                elif transformABC == transform2:
                    return 2
                elif transformABC == transform3:
                    return 3
                elif transformABC == transform4:
                    return 4
                elif transformABC == transform5:
                    return 5
                elif transformABC == transform6:
                    return 6
                elif transformABC == transform7:
                    return 7
                elif transformABC == transform8:
                    return 8



        return -1
