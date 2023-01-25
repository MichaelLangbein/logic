# https://replit.com/talk/learn/How-To-Make-a-Tensor-Class/27670


import random


def product(arr):
    i = 1
    for x in arr: i*= x
    return i


class Tensor:
    def __init__(self, arr=[]):
        self.__arr = self.process(arr)
        self.dimensions = self.getDims()

    def __len__(self):
        return len(self.__arr)

    def __getitem__(self, index):
        return self.__arr[index]

    def getDims(self):
        dims = []
        dims.append(len(self.__arr))
        if type(self.__arr[0]) == Tensor:
            dims += self.__arr[0].getDims()
        return dims

    def process(self, arr):
        newArr = []
        for i in arr:
            if type(i) == list:
                newArr.append(Tensor(i))
            else:
                newArr.append(i)
        return newArr

    def asArray(self):
        arr = []
        isVector = len(self.dimensions) == 1
        for i in self.__arr:
            if isVector:
                arr.append(i) 
            else:
                arr.append(i.asArray())
        return arr

    def asVector(self):
        vector = []
        isVector = len(self.dimensions) == 1
        for i in self.__arr:
            if isVector:
                vector.append(i)
            else:
                vector += i.asVector()
        
        return vector

    def package(array1D, dims):
        if len(array1D) == 1:
            return array1D[0]

        newarr = []

        index = 0
        p = product(dims[1:])
        for i in range(dims[0]):
            newarr.append(Tensor.package(array1D[index:index+p], dims[1:]))
            index += p

        return Tensor(newarr)

    def zeros(*dims):
        arr = [0] * product(dims)
        if len(dims) == 1:
            return Tensor(arr)
        return Tensor.package(arr, dims)

    def eye(*dims):
        arr = []
        for d, dim in enumerate(dims):
            for i in range(dim):
                if i == d:
                    arr.append(1.0)
                else:
                    arr.append(0.0)
        if len(dims) == 1:
            return Tensor(arr)
        return Tensor.package(arr, dims)

    def rand(*dims):
        arr = []
        for i in range(product(dims)):
            arr.append(random.random())
        if len(dims) == 1: 
            return Tensor(arr)
        return Tensor.package(arr, dims)

    def transpose(self, order=[]):

        # If tensor is an array, aka 1-dimensional, transpose is identical.
        if len(self.dimensions) == 1:
            return Tensor(self.__arr)

        # No particular order passed, so just reverse dimensions.
        # If dimensions were [2, 4, 6, 3] they become [3, 6, 4, 2].
        if not order:
            order = list(reversed(range(len(self.dimensions))))

        newDims = [self.dimensions[i] for i in order]

        arr = Tensor.zeros(*newDims).asArray()

        # go through all possible paths in the tensor
        paths = [0]*len(self.dimensions)
        while paths[0] < self.dimensions[0]:
         
            # get references to the path, put the number in the tensor to its corresponding spot in the new tensor
            ref = self
            place = arr
            for i in range(len(paths) - 1):
                ref = ref[paths[i]]
                place = place[paths[order[i]]]
            
            place[paths[order[-1]]] = ref[paths[-1]]

            # GROUP 4
            # go to the next path (sequentially)
            paths[-1] += 1
            for i in range(len(paths)-1, 0, -1):
                if paths[i] >= self.dimensions[i]:
                    paths[i] = 0
                    paths[i-1] += 1
                else: 
                    break

        return Tensor(arr)


    def __add__(self, other):
        newarr = []

        # If input is a scalar, just add it to all elements
        if type(other) != Tensor:
            for i in self.__arr:
                newarr.append(i + other)

        else:
            for i in range(len(self.__arr)):
                val = self.__arr[i] + other[i]
                newarr.append(val)

        return Tensor(newarr)
        

    def __mul__(self, other):
        newarr = []

        if type(other) != Tensor:
            for i in self.__arr:
                newarr.append(i * other)

        else:
            for i in range(len(self.__arr)):
                val = self.__arr[i] * other[i]
                newarr.append(val)

        return Tensor(newarr)


    def __neg__(self, other):
        return self * -1


    def __sub__(self, other):
        return self + (-other)


    def __truediv__(self, other):
        newarr = []

        if type(other) != Tensor:
            for i in self.__arr:
                newarr.append(i / other)

        else:
            for i in range(len(self.__arr)):
                val = self.__arr[i] / other[i]
                newarr.append(val)

        return Tensor(newarr)


    def __floordiv__(self, other):
        newarr = []

        if type(other) != Tensor:
            for i in self.__arr:
                newarr.append(i/other)
                
        else:
            for i in range(len(self.__arr)): 
                newarr.append(self.__arr[i] // other[i])
                
        return Tensor(newarr)


    # [1, 2, 3] + [4, 5, 6] = [1, 2, 3, 4, 5, 6]
    def directSum(self, other):
        if other.dimensions[1:] == self.dimensions:
            return Tensor(self.asArray() + other.asArray())
        
    
    # [1, 2]*[3, 4] = [1*3, 1*4, 2*3, 2*4].
    def tensorProduct(self, other):
        newarr = []

        for i in range(len(self)):
            for j in range(len(other)):
                if len(self.dimensions) == 1 or len(other.dimensions) == 1:
                    newarr.append(self[i] * self[j])
                else:
                    newarr.append()


    def __str__(self):
        ret = "\n["
        commas = False
        if type(self.__arr[0]) is not Tensor: commas = True
        for i in self.__arr:
            ret += str(i)
            if commas: ret += ', '
                
        if commas:
            ret = ret[:-2]
        else:
            ret += '\n'
        ret += ']'

        for i in range(len(ret) - 2, 0, -1):
            if ret[i] == '\n' and ret[i+1] in '[]' and ret[i-1] == ret[i+1]:
                ret = ret[:i] + ret[i+1:]

        return ret


    def matmul(self, other):

        # If both arguments are 2-D they are multiplied like conventional matrices.
        # If either argument is N-D, N > 2, it is treated as a stack of matrices residing in the last two indexes and broadcast accordingly.
        # If the first argument is 1-D, it is promoted to a matrix by prepending a 1 to its dimensions. After matrix multiplication the prepended 1 is removed.
        # If the second argument is 1-D, it is promoted to a matrix by appending a 1 to its dimensions. After matrix multiplication the appended 1 is removed.

        def firstVector(v, m):
            v = Tensor([v])
            return Tensor.matmul(v, m)[0]

        def secondVector(m, v):
            v = Tensor([[v[i]] for i in range(len(v))])
            r = Tensor.matmul(m, v)
            return Tensor([r[i][0] for i in range(len(r))])

        def matrices(m1, m2):

            newarr = []

            for _ in range(m1.dimensions[0]):
                newarr.append([0]*m2.dimensions[1])
                        
            for i in range(m2.dimensions[1]): # for all columns in the second matrix
                for j in range(m1.dimensions[0]): # for all rows in the first matrix
                    newarr[j][i] = sum([m2[k][i] * m1[j][k] for k in range(m1.dimensions[1])]) # for all numbers in the row of the first matrix
            
            return Tensor(newarr)
        
        def nd(nm1, nm2): # treat as a stack of matrices
            newarr = []
            if len(nm1.dimensions) > 2:
                for i in range(nm1.dimensions[0]):
                    newarr.append(nm1[i].matmul(nm2))
                return Tensor(newarr)

            elif len(nm2.dimensions) > 2:
                for i in range(nm2.dimensions[0]):
                    newarr.append(nm1.matmul(nm2[i]))
                return Tensor(newarr)
            
            
        if len(self.dimensions) == 1 and len(other.dimensions) == 2:
            return firstVector(self, other)
        elif len(self.dimensions) == 2 and len(other.dimensions) == 1:
            return secondVector(self, other)
        elif len(self.dimensions) == 2 and len(other.dimensions) == 2:
            return matrices(self, other)
        else:
            return nd(self, other)

    def __matmul__(self, other):
        return self.matmul(other)



