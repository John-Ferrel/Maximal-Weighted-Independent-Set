import scanpy as sc
import random
file="3elt.mtx"
adata = sc.read(file)
data = adata.X
data=data.todense()
data=data.A
data=data.tolist()
datai=[[str(int(x)) for x in i] for i in data]
random.seed(100)
weight=[str(random.randint(1,100)) for i in range(len(datai))]  #使用的随即权重
with open("3elt_text.txt",'w') as f:
    f.write(str(len(datai))+'\n')
    f.write(str(' '.join(weight)+'\n'))
    for i in datai:
        f.write(' '.join(i)+'\n')
    f.close()
print('程序已运行完毕')