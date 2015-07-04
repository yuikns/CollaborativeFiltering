import math


class CollaborativeFiltering(object):
    def __init__(self, x_train):
        self.x_train = x_train

    def sim(self, i, j ) : # cos
        il = []
        jl = []
        for k,v in i.iteritems():
            if k in j :
                il.append(v)
                jl.append(j[k])
        if len(il) == 0 :
            return 0
        else :
            deno = 0
            numx = 0
            numy = 0
            for i in range(len(il)):
                deno += il[i] * jl[i]
                numx += il[i] * il[i]
                numy += jl[i] * jl[i]
            if numx == 0 or numy == 0 :
                return 0
            else :
                return deno / ( math.sqrt(numx) * math.sqrt(numy) )

    def score(self, i, j , pred = True):
        if i in x and j in x[i] :# score is also given
            return x[i][j]
        elif not pred : # not predict
            return 0
        else :
            score_sum = 0
            sim_sum = 0
            for k in x.keys() :
                if k != i : # skip himself
                    k_score = self.score(k, j, False) # not predict , get the score
                    csim = self.sim(x[i],x[k])
                    if k_score > 0 and csim > 0 : # if k_score is zero , it means that the score is not setted
                        sim_sum += csim
                        score_sum += csim * k_score
            if sim_sum == 0 :
                return 0
            else :
                return score_sum / sim_sum

    def predict(self, x_t, i , j):
        score_sum = 0
        sim_sum = 0
        for k in x.keys() :
            k_score = self.score(k, j, False) # not predict , get the score
            csim = self.sim(x_t[i],x[k])
            if k_score > 0 and csim > 0 : # if k_score is zero , it means that the score is not setted
                sim_sum += csim
                score_sum += csim * k_score
        if sim_sum == 0 :
            return 0
        else :
            return score_sum / sim_sum

    # evaluation
    def rmse(self, x_t) :
        counter = 0
        all_sum = 0
        for k,v in x_t.iteritems():
            for t,s in v.iteritems() : # k-t => s(real score) sp(predicted score)
                sp = self.predict(x_t,k,t)
                if sp != 0 :
                    print "i:",k,"j:",t,"real:",s,"predict:",sp
                    counter += 1
                    all_sum += (sp - s) * (sp - s)
                    print "counter:",counter,"all sum:",all_sum
        #return deno / ( math.sqrt(numx) * math.sqrt(numy) )
        if counter == 0  or all_sum <= 0 :
            return -1
        else :
            print "val:" , (all_sum / counter)
            return math.sqrt(all_sum / counter)

if __name__ == "__main__":
    # matrx
    # train data
    x = {}
    x[1] = {}
    x[1][0] = 1
    x[1][1] = 3
    x[1][2] = 5
    x[1][3] = 2
    x[2] = {}
    x[2][0] = 2
    x[2][1] = 1
    x[2][2] = 3
    x[2][3] = 1
    x[3] = {}
    x[3][0] = 3
    x[3][1] = 3
    x[3][2] = 5
    x[3][3] = 1
    x[4] = {}
    x[4][0] = 3
    x[4][1] = 3
    x[4][2] = 5
    #x[4][3] = 0

    # test data
    x_t = {}
    x_t[5] = {}
    x_t[5][0] = 1
    x_t[5][1] = 3
    x_t[5][2] = 5
    x_t[5][3] = 2

    cf = CollaborativeFiltering(x)
    print "sim:",cf.sim(x[1],x[2])

    print "score :",cf.score(4,3)
    print "predict :",cf.predict(x_t,5,3)
    print "rmse :",cf.rmse(x_t)

    print "done"


