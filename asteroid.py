N=5
K=2
fuel=0

asteroid1 = [1,0,0,0,0]
asteroid2 = [0,0,0,1,0]
asteroid3 = [0,0,0,0,1]
asteroid4 = [1,0,0,0,0]
asteroid5 = [0,0,0,0,1]
me= asteroid1[2]

if asteroid1[0]+asteroid1[1]+asteroid1[3]+asteroid1[4]==1:
    fuel = K-distance_i+1