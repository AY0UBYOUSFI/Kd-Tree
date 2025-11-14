import numpy as np

point_group = [
    [1,1],
    [4,20],
    [5,15],
    [8,30],
    [7,3],
    [10,20],
    [14,50],
    [16,65],
    [17,60],
    [18,80],
    [19,70]
]

data = np.array(point_group)
# new_point = np.array([11,30])
new_point = np.array([11,15])

superDist = 9999999999
BestClass = np.array([])
ThreeB = np.array([])
ThreeB=np.reshape(ThreeB,(-1,2))
dB = np.array([])



class Kd_tree:
    def __init__(this):
        this.root = None
        this.left = None
        this.right = None

    def GenerateKdTree(this, data, dp):
        (size, _) = np.shape(data)
        if size == 0:
            return None
        index = size // 2
        if dp % 2 == 0:
            data = data[data[:, 0].argsort()]
        else:
            data = data[data[:, 1].argsort()]
        this.root = data[index, :]
        left = data[:index, :]
        right = data[index + 1:, :]
        dp += 1
        this.left = Kd_tree()
        this.left.GenerateKdTree(left, dp)
        this.right = Kd_tree()
        this.right.GenerateKdTree(right, dp)
        return this

def EcD(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def Branch(point, node, distance, level):
    if level % 2 == 0:
        d = abs(point[0] - node[0])
    else:
        d = abs(point[1] - node[1])
    return d < distance

def test(node, query):
    global superDist, BestClass, ThreeB,dB
    # ThreeB=np.reshape(ThreeB,(-1,2))
    dis = EcD(node, query)

    print("dist : ",dis,"node is :",node)
    if(len(ThreeB)<3):
        ThreeB = np.append(ThreeB,[node],axis=0)
        dB = np.append(dB,dis)
        
    else:
        if(dis < np.max(dB)):
            index = np.argmax(dB)
            
            print("\nindex : ",ThreeB[index,:]," <--> ",node)
            ThreeB[index,:] = node
            dB[index] = dis

    if dis < superDist:
        superDist = dis
        BestClass = node

        
        

def findBest(tree, p, level=0):
    global superDist, BestClass
    if tree is None or tree.root is None:
        return
    if level % 2 == 0:
        if p[0] < tree.root[0]:
            findBest(tree.left, p, level + 1)
        else:
            findBest(tree.right, p, level + 1)
    else:
        if p[1] < tree.root[1]:
            findBest(tree.left, p, level + 1)
        else:
            findBest(tree.right, p, level + 1)
    test(tree.root, p)
    if Branch(p, tree.root, superDist, level):
        if level % 2 == 0:
            if p[0] < tree.root[0]:
                findBest(tree.right, p, level + 1)
            else:
                findBest(tree.left, p, level + 1)
        else:
            if p[1] < tree.root[1]:
                findBest(tree.right, p, level + 1)
            else:
                findBest(tree.left, p, level + 1)

def P_gd(tree):
    if tree != None and tree.root is not None:
        P_gd(tree.left)
        print(tree.root)
        P_gd(tree.right)

delta = Kd_tree()
delta.GenerateKdTree(data, 0)

findBest(delta, new_point)

print("\nthe best class is : ", BestClass)
print("\nwith distance of : ", superDist)
ThreeB = np.array(ThreeB)
print("\nmy k array : ", ThreeB)
print("\ndB :",dB.round(2))
