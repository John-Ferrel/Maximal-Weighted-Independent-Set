# Documentation

### Pretreatment

We use 3 graphs to evaluate our algorithm. All of them can be found in "networkrepository.com".
Since most of the graphs don't have vertex weights, to those graphs, we first transform them into edge-unweighted and undirected graph, and then weight those vertexs with weights which satisfy normal distribution.
Since we just run our algorithm on our private computer, we should first cut some graph into small subgraphs. For example, 'astro_ph_s' comes from 'astro-ph' which has nearly 20,000 vertex.
During cutting the graphs, we use two strategys : 'smaller' and 'smaller_2'. 
In 'smaller', we randomly choose some vertexs from the original graph to form the new graph. In 'smaller_2', we delete some vertexs whoose degree is too small. In this way, we could get a relativly dense and smaller graph.
After pretreatment, we get vertex-weighted, undirected graphs with about 200~2000 vertexs.

---

### Main process

#### 1.Input

The first line is the number of vertices
The second line is the weight of each vertex
Each remaining rows are the adjacency relationships of each node

example:

```txt
10
5 75 24 75 46 9 65 41 83 20
0 1 1 0 0 0 0 0 0 0
1 0 0 1 0 0 0 0 0 0
1 0 0 0 1 1 1 0 0 0
0 1 0 0 0 0 0 0 0 1
0 0 1 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0
0 0 1 0 0 0 0 1 1 0
0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 1 0 0 0
0 0 0 1 0 0 0 0 0 0
```

The above data is placed in the txt file

#### 2.Output

Independent set, total weight, pruning node and process time in six cases.

example:

```python
------------------------------------------------------------
greedyFeature= newRate ,pruning= True :
MWIS: [2, 3, 5, 15, 16, 19, 21, 24, 25, 26, 31, 32, 34, 36, 41, 42, 49, 53, 55, 56, 58, 60, 61, 62, 66, 67, 68, 69, 70, 71, 73, 75, 76, 77, 79, 87, 88, 89, 91, 96, 101, 107, 108, 111]
totalWeight: 3006.0
cutoff1_index_set: [32, 67, 108, 25, 34, 3, 19, 75, 62, 21, 26, 41, 60, 53]
cutoff2_index_set: [49, 61, 55, 96, 71, 77, 31, 24, 2, 91, 58, 111, 76, 89, 107, 66]
process time: 33.90669822692871 ms
```



#### 3.GreedyFeature

There are 3 greedy Features in greedy algorithm.
$$
weightPerNumPlusOne=node.weight / (node.degreeNumber + 1)\\
adjWeiRate = node.weight / (node.weight +\sum node.adj.weight)\\
newRate = 2 \times adjWeiRate \times weightPerNumPlusOne\\
$$
Because  $adjWeiRate \in (0,1]$,  and pruning only when $adjWeiRate \ge 0.33$. Constant `2` is used to adjust the coefficient `adjWeiRate` around 1.

