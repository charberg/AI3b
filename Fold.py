from Feature import Feature
from Class import Class
import random
from sklearn import tree
from sklearn.datasets import load_iris
import csv

class Fold:

    class1 = []
    class2 = []
    class3 = []


    def crossValidation(self):
        folds = 5

        correct = [0,0,0]
        confusion = [[0 for x in range(3)] for y in range(3)]
        confusion2 = [[0 for x in range(3)] for y in range(3)]
        trainData = []
        trainClasses = []
        binSize1 = len(self.class1)/folds
        binSize2 = len(self.class2)/folds
        binSize3 = len(self.class3)/folds

        #Divide each collection into size of FOLDS, train on FOLDS - 1, test on remaining.
        for fold in range(0, folds):
            odds1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            odds2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            odds3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]



            #TRAIN
            for i in range(0,len(self.class1)):
                #Check if in testing range, if so, pass
                if binSize1*fold <= i and i < binSize1*(fold+1):
                    continue
                #In training range, add feature to feature count per respective class
                for j in range(0, len(self.class1[i].features)):
                    odds1[j] = odds1[j] + self.class1[i].features[j]

                #Get training data for decision tree
                trainData.append(self.class1[i].features)
                trainClasses.append(1)


            for i in range(0,len(self.class2)):
                #Check if in testing range, if so, pass
                if binSize2*fold <= i and i < binSize2*(fold+1):
                    continue
                #In training range, add feature to feature count per respective class
                for j in range(0, len(self.class2[i].features)):
                    odds2[j] = odds2[j] + self.class2[i].features[j]

                #Get training data for decision tree
                trainData.append(self.class2[i].features)
                trainClasses.append(2)


            for i in range(0,len(self.class3)):
                #Check if in testing range, if so, pass
                if binSize3*fold <= i and i < binSize3*(fold+1):
                    continue
                #In training range, add feature to feature count per respective class
                for j in range(0, len(self.class3[i].features)):
                    odds3[j] = odds3[j] + self.class3[i].features[j]

                #Get training data for decision tree
                trainData.append(self.class3[i].features)
                trainClasses.append(3)

            #Train decision tree
            clf = tree.DecisionTreeClassifier()
            clf = clf.fit(trainData, trainClasses)

            #TEST
            #At this stage, go through testing range
            #Start by dividing odds to percentage
            for i in range(0, len(odds1)):
                odds1[i] = odds1[i]/(len(self.class1)-binSize1)
            for i in range(0, len(odds2)):
                odds2[i] = odds2[i]/(len(self.class2)-binSize2)
            for i in range(0, len(odds3)):
                odds3[i] = odds3[i]/(len(self.class3)-binSize3)


                #Attempt to classify classes in test range
        for j in range(0, len(self.class1)):
            guess = self.classify(odds1, odds2, odds3, self.class1[j])
            confusion[0][guess-1]+=1
            guess2 = clf.predict([self.class1[j].getBinaryData()])[0]
            confusion2[0][guess2-1]+=1
            if guess == 1:
                correct[0]+=1

        for j in range(0, len(self.class2)):
            guess = self.classify(odds1, odds2, odds3, self.class2[j])
            confusion[1][guess-1]+=1
            guess2 = clf.predict([self.class2[j].getBinaryData()])[0]
            confusion2[1][guess2-1]+=1
            if guess == 2:
                correct[1]+=1

        for j in range(0, len(self.class3)):
            guess = self.classify(odds1, odds2, odds3, self.class3[j])
            confusion[2][guess-1]+=1
            guess2 = clf.predict([self.class3[j].getBinaryData()])[0]
            confusion2[2][guess2-1]+=1
            if guess == 3:
                correct[2]+=1


        print(len(self.class1))
        self.printConfusion(confusion)
        self.printConfusion(confusion2)

        iris = load_iris()
        tree.export_graphviz(clf, out_file='AI3b.dot')


    def classify(self, odds1, odds2, odds3, c):
        scores = [0,0,0]

        for i in range(0, len(odds1)):
            if c.hasFeature(i):
                scores[0] = scores[0] + odds1[i]
                scores[1] = scores[1] + odds2[i]
                scores[2] = scores[2] + odds3[i]

        return scores.index(max(scores))+1


    def printConfusion(self, conf):
        print("CONFUSION MATRIX:\n")
        for i in conf:
            print(i)

    def createClasses(self):
        avgv = [13.0,2.34,2.37,19.5,99.74,2.23,2.03,0.36,1.59,5.06,0.96,2.61,746.89]

        with open("wine.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                colCount = 0
                feats = []
                classNum = 0
                for col in row:
                    if colCount == 0:
                        classNum = int(col)
                        colCount += 1
                        continue

                    if float(col) > avgv[colCount-1]:
                        feats.append(1)
                    else:
                        feats.append(0)

                    colCount += 1
                if classNum == 1:
                    self.class1.append(Class(feats))
                elif classNum == 2:
                    self.class2.append(Class(feats))
                elif classNum == 3:
                    self.class3.append(Class(feats))

        print(len(self.class1))
        print(len(self.class2))
        print(len(self.class3))

if __name__ == '__main__':
    f = Fold()
    f.createClasses()
    f.crossValidation()