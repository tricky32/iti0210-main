Search Algorithm Performance Results




map size        algorithm     time(s)     iterations      path lenght (steps)
300x300         bfs           0.1321      47233           555
                greedy        0.0120      3358            983
                a*            0.0299      8202            555

600x600         bfs           0.5033      197804          1248
                greedy        0.0209      6293            1974
                a*            0.2203      60472           1248      

900x900         bfs           1.2088      450414          1844
                greedy        0.0967      29496           4130
                a*            0.3496      93999           1844




summary:

BFS: Tends to visit most cells on the map, so it takes longer but guarantees an optimal solution.
Greedy: Typically faster but can return suboptimal paths as it prioritizes closer nodes to the goal.
A*: Strikes a balance, usually faster than BFS and often finds the optimal path by considering both path cost and proximity to the goal.