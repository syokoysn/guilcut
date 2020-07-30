class One_cut :
    '''一つの問題例に対して、求解する calss 
    前提として,各 item に対して h > wが成り立つ
    Parameters
    ----------
    I : array_like 
        itemのlist 
    W_max : int
        W の上限
    H_max : int
        H の上限
    w : dict
        各 item の幅
    h : dict
        各item の高さ
    area :
        各 item の面積
    '''
    def __init__(self, I, W_max, H_max, w, h, area, df_item_data, mode = 'no'):
        self.I = I
        self.W_max = W_max; self.H_max = H_max
        self.W_min = 100
        self.df_item_data = df_item_data
        self.w = w; self.h = h
        self.area = area
        self.opt_time = None
        # 段数 K を作成。
        ''' I の中で一番小さいitemを基準に作成'''
        s_item = sorted(w.values())
        s = 0;k = 0
        for i in sorted(w.values()) :
            s  += i
            if H_max < s :
                break
            else:
                k += 1
        
        if k > len(I) :
            self.K = len(I)
        else :
            self.K = k
        print('K',self.K) 
        self.mode = mode
        if mode == 'r':
            # 妥当不等式のためのlist作成
            self.reasonable = []
            for a in range(len(self.I)):
                for b in range(a+1, len(self.I)) :
                    i, j = (a,b) if h[I[a]] > h[I[b]] else (b,a)
                    self.reasonable.append((i,j))
                    
    def __str__(self):
        return 'item {}, max(W,H) = ({},{})'.format(self.I,self.W_max,self.H_max)
        
    def make_sequence(self):
        '''順序制約のある組みのtupleを保持したリストを作成'''
        df = self.df_item_data
        use_stack = set([df.loc[df.ITEM_ID == i, 'STACK'][i] for i in self.I ])
        self.sequence = []
        for s in use_stack :
            flag = df[df.STACK == s].ITEM_ID.tolist()
            for i in range(len(flag)-1):
                if (flag[i] in self.I) & (flag[i+1]in self.I) :
                    self.sequence.append((flag[i],flag[i+1]))
        return 
    
    def solve(self, name = '') :
        '''求解'''
        self.make_sequence()
        self.model = gb.Model(name)
        W = self.model.addVar(vtype='I', name = 'W')
        H = self.model.addVar(vtype='I', name = 'H')
        x, y, hs, s = {}, {}, {}, {} # は定式化の sk　を表す
        r ,q = {},{}
        for k in range(self.K) :
            for i in self.I :
                x[i, k] = self.model.addVar(vtype='B',name = 'x{}_{}'.format(i,k)); y[i, k] = self.model.addVar(vtype='B',name = 'y{}_{}'.format(i,k))
                q[i,k] = self.model.addVar(vtype='B',name = 'q{}_{}'.format(i,k))
            hs[k] = self.model.addVar(vtype='I', name = 'h_{}'.format(k)) ;s[k] = self.model.addVar(vtype='B', name = 's_{}'.format(k)) 
            r[k] = self.model.addVar(vtype='B', name = 'r_{}'.format(k)) 
        z = self.model.addVar(vtype='B', name = 'z')
        for i in self.I :
            self.model.addConstr(gb.quicksum(x[i, k]+y[i, k] for k in range(self.K) ) == 1) #1
            for k in range(self.K):
                self.model.addConstr(self.h[i]*x[i, k]+self.w[i]*y[i, k] <= hs[k] - 20*(1- q[i,k]))#8-1
                self.model.addConstr(self.h[i]*x[i, k]+self.w[i]*y[i, k] >= hs[k]- self.H_max*(1- q[i,k]))#8-2
        for k in range(self.K):
            self.model.addConstr(gb.quicksum(self.w[i]*x[i, k]+ self.h[i]*y[i, k] for i in self.I) <= W - 20*(1-r[k])) #2-1
            self.model.addConstr(gb.quicksum(self.w[i]*x[i, k]+ self.h[i]*y[i, k] for i in self.I) >= W - self.W_max*(1-  r[k])) #2-2
            self.model.addConstr(hs[k] <= 0 + self.H_max*(1- s[k]))# 7.1
            self.model.addConstr(100 <= hs[k] + 100*s[k])# 7.2
            if (0 < k) :#&(len(self.I)):
                self.model.addConstr(gb.quicksum(x[i,k-1]+ y[i, k-1] for i in self.I) >= (1/len(self.I)) * gb.quicksum(x[i, k]+ y[i, k] for i in self.I))# 10
            #妥当不等式
            if self.mode == 'r':
                for i, j in self.reasonable :
                    if self.h[self.I[i]] - 20 >= self.h[self.I[j]]:
                        if self.w[self.I[i]] -20>= self.h[self.I[j]]:
                            self.model.addConstr(x[self.I[i],k]+y[self.I[i],k]+y[self.I[j],k]<=1)
                        else :
                            self.model.addConstr(x[self.I[i],k]+y[self.I[j],k]<=1)
        self.model.addConstr(W <= self.W_max)# 3
        self.model.addConstr(gb.quicksum(hs[k] for k in range(self.K)) == H)# 4
        self.model.addConstr(H <= self.H_max)# 5
        self.model.addConstr(H <= 3190 +20*(1-z))#6.1
        self.model.addConstr(self.H_max <= H +self.H_max*z )#6.2
        if self.W_max <3500 :
            zz = self.model.addVar(vtype='B', name = 'zz')#追加
            self.model.addConstr(W >=self.W_max *(1-zz))#追加
            self.model.addConstr(W<= self.W_max -20*zz)#　追加
        for i, j in self.sequence:
            for k in range(0, self.K):
                self.model.addConstr( gb.quicksum(x[i, p] + y[i, p] for p in range(0, k+1)) >= x[j, k] + y[j, k] )# 9
        self.model.update()
        self.model.setObjective(W, gb.GRB.MINIMIZE)
        s = time.time()
        self.model.optimize()
        e = time.time()
        self.opt_time = e-s
        #self.model.display()
        self.status = self.model.status
        if self.status  == gb.GRB.Status.OPTIMAL :
            self.OPT = self.model.ObjVal
            self.filling_rate = (self.area[self.I].sum()) /(self.H_max*self.model.ObjVal)