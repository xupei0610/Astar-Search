#Description

This is the repository for the code of the project of _**Comparison of Search Algorithms**_.

#Author
Pei Xu, 5186611, xuxx0884 at umn.edu

#License
MIT

#Files
The complete code contains 4 file except the readme file:

  1. _**Astar.py**_ is the library file of A* search.
  
  It has a solver function and a Node class as the interface of node used in the solver function.
    
  2. _**SlidingPuzzle.py**_ is the library file of Sliding Puzzle.
  
  It has a function to generate a puzzle's initial state, a function to generate a initial node using the Node class defined in this file which is a realization of the interface Astar.Node(), and a static class who has the realization of 3 heuristic algorithms (Manhattan Distance, Straight Line Distance and Squared Euclidean Distance).
    
  3. _**sptest.py**_ is the **main** program who can run test.
    
  4. _**sptest.sample.log**_ is a testing log who recoded a 10000-case testing results the author ran on Oct. 17th.
  
  The sptest file uses this file for a sample testing analysis.

# Algorithms
In my code, 9 kinds of algorithms will be tested, They are
 
    A* and Bi-A*: Manhattan, StraightLine, SquaredEuclid Distance
    
    GBFS: Manhattan, StraightLine, SquaredEuclid Distance

# Conclusions
5 conclusions we expect to reach through running tests:

    1: Manhattan Distance is better than Straight-Line Distance in sliding puzzle problem.
    2: Manhattan Distance and Straight-Line Distance can be used to find the optimal solution.
    3: Squared Euclidean Distance cannot find optimal solutions but is faster than the above two.
    4: Greedy Best-First Search cannot find optimal solutions but is faster than the above three.
    5: Bidirectional A* Search is not optimal but faster than A* Search when the depth is deep enough.
    
#Metrics:
  1. the average amount of _**nodes generated**_ during solving a puzzle
    
  It will be used to measure the time and space complexity.
    
  2. the average _**length of the solution**_ found by an algorithm
    
  It will be used to measure the optimality of that algorithm.
    
  3. the average _**running time**_ for solving a puzzle
    
  It will be shown, and it, in theory, should be directly proportional to the time and space complexity.

#Usage

Please run '_*python sptest -h*_' for more information about how to run a test using this file.

Tips:

    Do Not Run 4x4 Testing unless your spare time is really enough.
    You can run a small test (10 test cases) via the command 'python sptest -e -a'.
    But some conclusions the author expects to reach may not be reached via a small test.

Or, you can run '_**python sptest -a**_' for an automatic analysis to the _**sptest.sample.log**_ who is the log file of a 10000-case test using 3x3 sliding puzzles.

#Sample Analysis Result

    XP-MacBook-Pro:Src XP$ python3 sptest.py -a
    Preparing analysis...
    Loading data from sptest.sample.log ...
    10000 cases have been loaded.
    Begin analyzing...
    pass: assert s_data['A*-manhattan'][case_no][0] == s_data['A*-straightLine'][case_no][0]
    pass: assert s_data['A*-manhattan'][case_no][1] <= s_data['A*-straightLine'][case_no][1]
    pass: assert s_data['A*-manhattan'][case_no][1] < s_data['A*-straightLine'][case_no][1]
    pass: assert s_data['A*-squaredEuclid'][case_no][0] > s_data['A*-manhattan'][case_no][0]
    pass: assert s_data['GBFS-manhattan'][case_no][0] > s_data['A*-manhattan'][case_no][0] or s_data['GBFS-straightLine'][case_no][0] > s_data['A*-manhattan'][case_no][0] or s_data['GBFS-squaredEuclid'][case_no][0] > s_data['A*-manhattan'][case_no][0]
    pass: assert sum(s_data['GBFS-manhattan'][case_no][1]) <= sum(s_data['A*-manhattan'][case_no][1])
    pass: assert sum(s_data['GBFS-straightLine'][case_no][1]) <= sum(s_data['A*-straightLine'][case_no][1])
    pass: assert sum(s_data['GBFS-squaredEuclid'][case_no][1]) <= sum(s_data['A*-squaredEuclid'][case_no][1])
    pass: assert s_data['GBFS-manhattan'][case_no][1] > s_data['A*-manhattan'][case_no][1] or s_data['GBFS-straightLine'][case_no][1] > s_data['A*-straightLine'][case_no][1] or s_data['GBFS-squaredEuclid'][case_no][1] <= s_data['A*-squaredEuclid'][case_no][1]
    pass: assert s_data['Bi-A*-manhattan'][case_no][0] > s_data['A*-manhattan'][case_no][0]
    pass: assert sum(s_data['Bi-A*-manhattan'][case_no][1]) <= sum(s_data['A*-manhattan'][case_no][1])
    pass: assert sum(s_data['Bi-A*-straightLine'][case_no][1]) <= sum(s_data['A*-straightLine'][case_no][1])
    pass: assert sum(s_data['Bi-A*-squaredEuclid'][case_no][1]) <= sum(s_data['A*-squaredEuclid'][case_no][1])
    pass: assert s_data['Bi-A*-manhattan'][case_no][1] > s_data['A*-manhattan'][case_no][1] or assert s_data['Bi-A*-straightLine'][case_no][1] > s_data['A*-straightLine'][case_no][1] or assert s_data['Bi-A*-squaredEuclid'][case_no][1] > s_data['A*-squaredEuclid'][case_no][1]
        
    Testing Results:
      Conclusion 1 reached. Manhattan Distance and Straight-Line Distance can be used to find the optimal solution.
      Conclusion 2 reached. Manhattan Distance is better than Straight-Line Distance.
      Conclusion 3 reached. Squared Euclidean Distance cannot find optimal solutions.
      Conclusion 4.1 reached. Greedy Best-First Search cannot find optimal solutions
      Conclusion 4.2 reached. Greedy Best-First Search, in general, is faster.
      Conclusion 4.3 reached. Greedy Best-First Search is not always faster.
      Conclusion 5.1 reached. Bidirectional A* Search cannot guarantee the optimality.
      Conclusion 5.2 reached. Bidirectional A* Search, in general, is faster than A* Search.
      Conclusion 5.3 reached. Bidirectional A* Search is not always faster than A* Search.
      
    All conclusions have been reached. Perfect tests.
        
    Table 1:  Average     Steps      Nodes        Time
    A*-straightLine:      21.981400  3806.333700  5.404034
    A*-manhattan:         21.981400  2450.191300  2.017821
    A*-squaredEuclid:     22.508000  589.313900   0.118520
    Bi-A*-straightLine:   22.946400  829.024500   0.162734
    Bi-A*-manhattan:      23.276400  783.521600   0.144273
    Bi-A*-squaredEuclid:  23.772800  432.951100   0.055180
    GBFS-squaredEuclid:   40.270000  280.916900   0.023563
    GBFS-manhattan:       43.978400  479.831000   0.061197
    GBFS-straightLine:    49.521600  449.850500   0.051895
      
    Table 2:  Average      Steps      Nodes        Time
    GBFS-squaredEuclid:    40.270000  280.916900  0.023563
    Bi-A*-squaredEuclid:   23.772800  432.951100  0.055180
    GBFS-straightLine:     49.521600  449.850500  0.051895
    GBFS-manhattan:        43.978400  479.831000  0.061197
    A*-squaredEuclid:      22.508000  589.313900  0.118520
    Bi-A*-manhattan:       23.276400  783.521600  0.144273
    Bi-A*-straightLine:    22.946400  829.024500  0.162734
    A*-manhattan:          21.981400  2450.191300 2.017821
    A*-straightLine:       21.981400  3806.333700 5.404034
      
    Table 3:  Average      Steps      Nodes        Time
    GBFS-squaredEuclid:    40.270000  280.916900   0.023563
    GBFS-straightLine:     49.521600  449.850500   0.051895
    Bi-A*-squaredEuclid:   23.772800  432.951100   0.055180
    GBFS-manhattan:        43.978400  479.831000   0.061197
    A*-squaredEuclid:      22.508000  589.313900   0.118520
    Bi-A*-manhattan:       23.276400  783.521600   0.144273
    Bi-A*-straightLine:    22.946400  829.024500   0.162734
    A*-manhattan:          21.981400  2450.191300  2.017821
    A*-straightLine:       21.981400  3806.333700  5.404034
