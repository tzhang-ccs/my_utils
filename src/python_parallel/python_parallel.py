class python_parallel:
    def __init__(self,dx,dy,px,py):
        self.dx = dx
        self.dy = dy
        self.px = px
        self.py = py
        self.data = []

    def parallel_partition_2d(self, data, debug=False):
        # dx: domain x size
        # dy: domain y size
        # px: process number x
        # py: process number y
        if debug:
            print("domain size x and y: ", self.dx, self.dy)
            print("process number x and y: ", self.px, self.py)

        # lx: block size x
        # ly: block size y
        lx = self.dx // self.px
        ly = self.dy // self.py
        if debug:
            print("block size x and y: ", lx, ly)

        # gx: x index
        # gy: y index
        gx = np.arange(0,self.dx,1)
        gy = np.arange(0,self.dy,1)

        # sx: start corner x
        # sy: start corner y
        sx=gx[0:self.px*lx:lx]
        sy=gy[0:self.py*ly:ly]
        if debug:
            print("start corner x and y: ", sx, sy)


        for i in sx:
            for j in sy:
                if i == sx[-1] and j != sy[-1]:
                    self.data.append(data[i:,j:j+ly])
                elif i != sx[-1] and j == sy[-1]:
                    self.data.append(data[i:i+lx,j:])
                elif i == sx[-1] and j == sy[-1]:
                    self.data.append(data[i:,j:])
                else:
                    self.data.append(data[i:i+lx,j:j+ly])
                    
    def run(self, fun):
        pool = mp.Pool(self.px * self.py)
        self.results_list = pool.map(fun, self.data)

    def reshape_results(self):
        self.results = np.empty([0,self.dy])

        for i in range(self.px):
            lx = self.results_list[i*self.py].shape[0]
            row = np.empty([lx,0])
            for j in range(self.py):
                row = np.concatenate([row, self.results_list[i*py+j]], axis=1)

            self.results = np.concatenate([self.results,row],axis=0)
            
