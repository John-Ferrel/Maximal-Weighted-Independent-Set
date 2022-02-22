graph = load("GD98_c.mat"); 
y = graph.Problem.aux.coord;
lin = graph.Problem.A;
gplot(lin,y,"*-")
for i = 1:112
    lin(i)
end