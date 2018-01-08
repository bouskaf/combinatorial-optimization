import numpy as np
def brat(P,R,D):
    ub=np.max(D)

    def inside(unused,solution,c):
        if unused==[]:
            if np.min(R[[i for i in range(len(P))]])==np.min(solution):
                a=np.min(solution)
                t=[i for i in range(len(solution))if solution[i]==a ][0]
                test=True
                for i in range(len(solution)-1):
                    a = a + p[t]
                    t = [i for i in range(len(solution)) if solution[i] == a]
                    if not a:
                        test=False
                        break
                if test:
                    return 1, c, solution
                else:
                    return 0, c, solution
            else:
                return 0,c,solution
        op=[np.min(R[unused]), c]
        lb=np.min(op)+np.sum([P[unused]],axis=1)
        if(lb>ub):
            return 0,-1,solution
        for i in unused:
            if(c+P[i]>D[i]):
                return  0,-1, solution

        minr =np.min(R[unused])
        if(minr <= c):

            for i in range(len(unused)):
                sol=list(solution)
                unu=list(unused)
                t=unused[i]
                if(r[t]>c):
                    continue
                s=max(c,R[t])
                sol[t]=s
                s=s+P[t]
                unu.remove(t)
                optimal, cf, solf=inside(unu,sol,s)
                if optimal==1:
                    return optimal,cf, solf
        else:
            for i in range(len(unused)):
                sol = list(solution)
                unu = list(unused)
                t = unused[i]
                s = max(c, R[t])
                sol[t] = s
                s = s + P[t]
                unu.remove(t)
                optimal,cf, solf = inside(unu, sol, s)
                if optimal == 1:
                    return optimal,cf, solf
        return optimal,cf,solf