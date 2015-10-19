# -*- coding:utf-8 -*-
__author__ = "Pei Xu, #5186611, xuxx0884@umn.edu"
__copyright__ = "Copyright 2015-, Pei Xu"
__license__ = "MIT"
__version__ = "1.0.1"
__date__ = "23:31, Oct. 17th, 2015"
""" This is the testing program, and the main program, of the project of Comparison of Search Algorithms.
Sliding Puzzle Problem is generated for testing A* Algorithms.

Please see the detailed testing conclusion at the end of this file ( begins at about Line 155).
This test program will generate a logger file during testing """

import time, logging, sys, getopt, os
from threading import Thread

import Astar, SlidingPuzzle

def main(argv):
  try:
    opts, args = getopt.getopt(argv[1:], 'hvec:s:af:t:', ['help', 'version', 'test', 'cases=', 'size=', 'analyze', 'file=', 'timeout='])
  except getopt.GetoptError as err:
    print(str(err))
    usage()
    sys.exit(2)

  do_test = False
  do_analysis = False
  cases = 10
  size = 3
  sample_log = 'sptest.sample.log'
  log_file = None
  time_out = 120
  
  for o, a in opts:
    if o in ('-h', '--help'):
      usage()
      sys.exit()
    elif o in ('-v', '--version'):
      version()
      sys.exit()
    elif o in ('-e', '--experiment'):
      do_test = True
    elif o in ('-c', '--cases'):
      cases = int(a)
    elif o in ('-s', '--size'):
      size = int(a)
    elif o in ('-a', '--analyze'):
      do_analysis = True
    elif o in ('-f', '--file'):
      log_file = str(a)
    elif o in ('-t', '--timeout'):
      time_out = int(a)
      
  if do_test == True:
    log_file = test(size = size, cases = cases, log_file = log_file, time_out = time_out)
  
  if do_analysis == True:
    if log_file == None:
      if do_test == True:
        sys.exit()
      else:
        log_file = sample_log
    analyze(log_file)
    sys.exit()
  
  if do_test == False and do_analysis == False:
    usage()
    sys.exit()

def usage():
  print(__file__ + ' - the testing program of the project of Comparison of Search Algorithms.')
  print('Author: %s'%__author__)
  print('Copyright: %s'%__copyright__)
  print('License: %s'%__license__)
  print('\nThis program will use sliding puzzle problems to test A* Search and Greedy Best-First Search and make a comparison of them.')
  print('\nDuring testing, a log file will be generated. Please give enough permissions to this file if you need to do testing.')
  print('The file sptest.sample.log attached with this file is a sample log generated during a test conducted on Oct.17th. It can be used to analyze, and demonstrate 5 conclusions we expect to reach via the test.')
  print('\n9 kinds of algorithms will be tested, They are\n  A* and Bi-A*: Manhattan, StraightLine, SquaredEuclid\n  GBFS and GBFS: Manhattan, StraightLine, SquaredEuclid')
  print('5 conclusions we expect to reach:')
  print("  1: Manhattan Distance is better than Straight-Line Distance in sliding puzzle problem.")
  print("  2: Manhattan Distance and Straight-Line Distance can be used to find the optimal solution.")
  print("  3: Squared Euclidean Distance cannot find optimal solutions but is faster than the above two.")
  print("  4: Greedy Best-First Search cannot find optimal solutions but is faster than the above three.")
  print("  5: Bidirectional A* Search, in general, is faster than A* Search (when the depth is deep enough) but cannot guarantee the optimality.")
  print('Metrics:')
  print('  1. The average amount of nodes generated during solving a puzzle will be used to measure the time and space complexity.')
  print('  2. The average length of the solution found by an algorithm will be used to measure the optimality of that algorithm.')
  print('  3. The average running time for solving a puzzle will be shown, and it, in theory, should be directly proportional to the time complexity and space complexity.')
  print('\nUsage:')
  print('  -h, --help: show this help information.\n')
  print('  -v, --version: show the current version of this file and the Astar and SlidingPuzzle library it uses.\n')
  print('  -e, --experiment: doing test according to given parameters.\n    E.G. \'' +__file__+ ' -t -c 10 -s 3\' will generate 10 3x3 sliding puzzles for test.\n')
  print('  -c, --cases: the amount of testing cases. Default value is 10.\n    For 3x3 game, 50 is suggested for the first time.\n')
  print('  -s, --size: the size of testing sliding puzzles. 3 for 3x3, 4 for 4x4 and the like. Default value is 3. Not recommend 5 or more.\n')
  print('  -a, --analyze: analyze the log file generated during testing. \n    E.G. \'' +__file__+ ' -t -a\' will do tests firstly and then analyze the testing results.\n    Or e.g.\'' +__file__+ ' -a -f sptest.sample.log\' will analyze the sample log file to prove the conclusion we expect to reach in this test.\n')
  print('  -f, --file: the log file used for analyze. Default value is sptest.sample.log.\n     This option is ignored for the combination option \'-t -a\'.\n')
  print('  -t, --timeout: the maximum time permitted for an algorithm to solve a puzzle. Default value is 120, namely 2 mins.\n    For solving 4x4 puzzle, it is better to set 120 or more.')
  print("")

def version():
  print('%s v%s %s' % (__file__, __version__, __date__))
  print('%s v%s %s' % (Astar.__file__, Astar.__version__, Astar.__date__))
  print('%s v%s %s' % (SlidingPuzzle.__file__, SlidingPuzzle.__version__, SlidingPuzzle.__date__))


def test(size, cases, log_file = None, time_out = 120):
  """ Doing test according to the given game size and amount of testing cases, and generate a log file named log_file.
  Return the name of the log file generated.
  Return None if test fails"""
  
  # Log File's name
  if log_file == None:
    log_file = 'sptest %s.log'%(time.strftime("%H.%M.%S %F", time.localtime()))
  else:
    log_file = str(log_file)

  if os.path.exists(log_file):
    print('A file whose name is the same to the log file prepared to generate has existed !!!')
    return None
  
  # List testing information
  print('Preparing testing...')
  print('The amount of testing cases: %d' % cases)
  print('The game size of sliding puzzle: %dx%d' % (size, size))
  print('The log file will be generated: %s' % log_file)
  print('The maximum time permitted for an algorithm to solve a puzzle: %ds' % time_out)
  
  # 3 kinds of heuristic algorithms
  heuristics = (SlidingPuzzle.Heuristics.manhattan, SlidingPuzzle.Heuristics.straightLine, SlidingPuzzle.Heuristics.squaredEuclid)
  # 3 kinds of search algorithms
  methods = ('A*', 'GBFS')
  # The function used to revise the solution path for bi-direcitonal search
  revsPath = SlidingPuzzle.Heuristics.revsPath
  
  # Using logger to recod testing results
  logger = logging.getLogger('sptest')
  logger.setLevel(logging.DEBUG)
  wh = logging.FileHandler(log_file)
  wh.setFormatter(logging.Formatter('%(asctime)s - SlidingPuzzleTest - %(message)s'))
  ch = logging.StreamHandler()
  ch.setFormatter(logging.Formatter('%(message)s'))
  logger.addHandler(wh)
  logger.addHandler(ch)
  
  # Decorator function used to generate logger and limit the solver's running time.
  total_run_time = [0]
  time_out_cases = [0]
  def testingDecorator(time_out, total_run_time, time_out_cases):
    def decorator(func):
      def nfunc(*args, **args2):
        class TimeOut(Thread):
          def __init__(self, _error = None):
            Thread.__init__(self)
            self._error = _error
          def run(self):
            try:
              self.result = []
              self.result.append(func(*args, **args2))
              self.result.append(time.time())
            except Exception as e:
              self._error = e
          def stop(self):
            if self.is_alive():
              self.stopped = True
        th = TimeOut()
        th.setDaemon(True)
        start_time = time.time()
        th.start()
        th.join(time_out)
        if th.is_alive():
          th.stop()
          result = [['',0], start_time]
          total_run_time[0] = total_run_time[0] + time.time() - start_time
          time_out_cases[0] = time_out_cases[0] + 1
        else:
          result = th.result
        if th._error is None:
          if len(args) > 3 and args[3] != None:
            method = "Bi-" + args[2]
          else:
            method = args[2]
          end_time = result[1]
          this_run_time = end_time - start_time
          total_run_time[0] = total_run_time[0] + this_run_time
          logger = logging.getLogger('sptest')
          logger.info('Method: %s - HeuristicFunction: %s - SolutionLength: %d - NodesGenerated: %d - TimeTaken: %f' % (method, args[0].__name__, len(result[0][0]), result[0][1], this_run_time))
          return result
        else:
          raise Exception(e)
      return nfunc
    return decorator
  
  # Decorate A* solver for generating logger and limiting running time
  @testingDecorator(time_out, total_run_time, time_out_cases)
  def searchTest(*args):
    return Astar.solve(*args)

  print("\nTest begins...")
  # Begin Testing
  for i in range(cases):
    initial_node = SlidingPuzzle.generateInitialNode(SlidingPuzzle.generateInitialState(size))

    logger.info('%dx%d Test Case %d. Initial State: %s'% (size, size, i+1, initial_node.getState()))
    
    for h in heuristics:
      for m in methods:
        searchTest(h, initial_node, m, None, None)
    
    goal_node = SlidingPuzzle.generateInitialNode(initial_node.getGoalState(), initial_node.getState())
    for h in heuristics:
      searchTest(h, initial_node, methods[0], goal_node, revsPath)

  print("\n%d cases have been tested.\n%d of them time out.\nTotal Time Taken: %fs\nLogger File Generated: %s"%(cases, time_out_cases[0], total_run_time[0], log_file))

def analyze(log_file):
  """ Analyze a log file generated via this testing program."""
  
  print('Preparing analysis...')
  
  print('Loading data from %s ...' % log_file)
  i = 1
  # s_data records algorithms' performance in each case
  # s_data = {search_method:[(solution length, no. of nodes generated, running time),...], ...}
  s_data = {}
  with open(log_file) as f:
    for line in f.readlines():
      if i%10 != 1:
        # Leap over the first line of a group of case
        # because this line is the case information we don't need
        gr = line.split(' - ')
        method = (gr[2].split(': '))[1] + '-' + (gr[3].split(': '))[1]
        if method not in s_data:
          s_data[method] = []
        s_data[method].append((int((gr[4].split(': '))[1]), int((gr[5].split(': '))[1]), float((gr[6].split(': '))[1])))
      i = i+1
  f.close()
  # no. of cases loaded
  cases = int((i-1)/10)
  print("%d cases have been loaded." % cases)
  # r_data used to do sum of s_data
  r_data = {}
  for x in s_data:
    r_data[x] = [0, 0, 0]
    
  print('Begin analyzing...')
  
  # Two Metrics are used.
  # 1. The Length of the found solution is used to prove the optimality.
  # 2. The Amount of nodes generated is used to prove their efficiency (time and space used).

  Manhattan_better_than_straightLine = False
  GBFS_not_optimal = False
  bi_A_not_always_optimal = False
  A_squaredEuclid_not_nece_optimal = False

  for case_no in range(cases):

    time_out_case = False
    for x in s_data:
      # Time-Outed Case
      if s_data[x][case_no][0] == 0:
        time_out_case = True

    if time_out_case == False:
      for x in s_data:
        r_data[x][0] = r_data[x][0] + s_data[x][case_no][0]
        r_data[x][1] = r_data[x][1] + s_data[x][case_no][1]
        r_data[x][2] = r_data[x][2] + s_data[x][case_no][2]
      
    # Conclusion 1:
    # A*-manhattan and A*Straight-Line are both optimal, namely, both of their solutions should be optimal.
    assert s_data['A*-manhattan'][case_no][0] == s_data['A*-straightLine'][case_no][0]
    assert s_data['A*-manhattan'][case_no][0] <= s_data['A*-squaredEuclid'][case_no][0]
    assert s_data['A*-manhattan'][case_no][0] <= s_data['GBFS-manhattan'][case_no][0]
    assert s_data['A*-manhattan'][case_no][0] <= s_data['GBFS-straightLine'][case_no][0]
    assert s_data['A*-manhattan'][case_no][0] <= s_data['GBFS-squaredEuclid'][case_no][0]
    assert s_data['A*-manhattan'][case_no][0] <= s_data['Bi-A*-manhattan'][case_no][0]
    assert s_data['A*-manhattan'][case_no][0] <= s_data['Bi-A*-straightLine'][case_no][0]
    assert s_data['A*-manhattan'][case_no][0] <= s_data['Bi-A*-squaredEuclid'][case_no][0]

    # Conlusion 2:
    # A*-manhattan should always not worse
    assert s_data['A*-manhattan'][case_no][1] <= s_data['A*-straightLine'][case_no][1]
    if s_data['A*-manhattan'][case_no][1] < s_data['A*-straightLine'][case_no][1]:
      Manhattan_better_than_straightLine = True
    
    # Conlusion 3
    # A*-squaredEduclid should be a little similar to GBFS, namely, relatively fast but not optimal
    assert s_data['A*-squaredEuclid'][case_no][0] >= s_data['A*-manhattan'][case_no][0]
    if s_data['A*-squaredEuclid'][case_no][0] > s_data['A*-manhattan'][case_no][0]:
      A_squaredEuclid_not_nece_optimal = True
    
    # Conclusion 4.1
    # GBFS are not necessarily able to find optimal solutions
    assert s_data['GBFS-manhattan'][case_no][0] >= s_data['A*-manhattan'][case_no][0]
    assert s_data['GBFS-straightLine'][case_no][0] >= s_data['A*-manhattan'][case_no][0]
    assert s_data['GBFS-squaredEuclid'][case_no][0] >= s_data['A*-manhattan'][case_no][0]
    if s_data['GBFS-manhattan'][case_no][0] > s_data['A*-manhattan'][case_no][0] or \
      s_data['GBFS-straightLine'][case_no][0] > s_data['A*-manhattan'][case_no][0] or \
      s_data['GBFS-squaredEuclid'][case_no][0] > s_data['A*-manhattan'][case_no][0]:
      GBFS_not_optimal = True
    
    # Conclusion 4.2
    # GBFS should be faster
    try:
      assert s_data['GBFS-manhattan'][case_no][1] <= s_data['A*-manhattan'][case_no][1]
      assert s_data['GBFS-straightLine'][case_no][1] <= s_data['A*-straightLine'][case_no][1]
      assert s_data['GBFS-squaredEuclid'][case_no][1] <= s_data['A*-squaredEuclid'][case_no][1]
    except Exception as e:
      GBFS_not_always_faster = True
    
    # Conclusion 5.1
    # Even Bi-directional A*-manhattan and A*-straightline, they are not necessarily able to find optimal solutions
    assert s_data['Bi-A*-manhattan'][case_no][0] >= s_data['A*-manhattan'][case_no][0]
    if s_data['Bi-A*-manhattan'][case_no][0] > s_data['A*-manhattan'][case_no][0]:
      bi_A_not_always_optimal = True
      
    # Conclusion 5.2
    # Bi-directional A* Search should be faster than corresponding Uni-directional A* Search when depth is deep enough
    try:
      assert s_data['Bi-A*-manhattan'][case_no][1] <= s_data['A*-manhattan'][case_no][1]
      assert s_data['Bi-A*-straightLine'][case_no][1] <= s_data['A*-straightLine'][case_no][1]
      assert s_data['Bi-A*-squaredEuclid'][case_no][1] <= s_data['A*-squaredEuclid'][case_no][1]
    except Exception as e:
      BiA_not_always_faster = True
  
  completed_conclusion = 0
  conclusions = []

  print("pass: assert s_data['A*-manhattan'][case_no][0] == s_data['A*-straightLine'][case_no][0]")
  conclusions.append('Conclusion 1 reached. Manhattan Distance and Straight-Line Distance can be used to find the optimal solution.')
  completed_conclusion = completed_conclusion + 1
  
  try:
    assert Manhattan_better_than_straightLine == True
    print("pass: assert s_data['A*-manhattan'][case_no][1] <= s_data['A*-straightLine'][case_no][1]")
    print("pass: assert s_data['A*-manhattan'][case_no][1] < s_data['A*-straightLine'][case_no][1]")
    conclusions.append("Conclusion 2 reached. Manhattan Distance is better than Straight-Line Distance.")
    completed_conclusion = completed_conclusion + 1
  except Exception as e: 
    print("pass: assert s_data['A*-manhattan'][case_no][1] <= s_data['A*-straightLine'][case_no][1]")
    print("not pass: assert s_data['A*-manhattan'][case_no][1] < s_data['A*-straightLine'][case_no][1]")
    conclusions.append("Conclusion 2 not reached. Manhattan Distance performed same to Straight-Line Distance in given testing cases.")
  
  try:
    assert A_squaredEuclid_not_nece_optimal == True
    print("pass: assert s_data['A*-squaredEuclid'][case_no][0] > s_data['A*-manhattan'][case_no][0]")
    conclusions.append("Conclusion 3 reached. Squared Euclidean Distance cannot find optimal solutions.")
    completed_conclusion = completed_conclusion + 1
  except Exception as e:
    print("pass: assert s_data['A*-squaredEuclid'][case_no][0] >= s_data['A*-manhattan'][case_no][0]")
    print("not pass: assert s_data['A*-squaredEuclid'][case_no][0] > s_data['A*-manhattan'][case_no][0]")
    conclusions.append("Conclusion 3 reached. Squared Euclidean Distance found optimal solutions.")

  try: 
    assert GBFS_not_optimal == True
    print("pass: assert s_data['GBFS-manhattan'][case_no][0] > s_data['A*-manhattan'][case_no][0] or s_data['GBFS-straightLine'][case_no][0] > s_data['A*-manhattan'][case_no][0] or s_data['GBFS-squaredEuclid'][case_no][0] > s_data['A*-manhattan'][case_no][0]:")
    conclusions.append("Conclusion 4.1 reached. Greedy Best-First Search cannot find optimal solutions")
    completed_conclusion = completed_conclusion + 1
  except Exception as e:
    print("pass: assert s_data['GBFS-manhattan'][case_no][0] >= s_data['A*-manhattan'][case_no][0]")
    print("pass: assert s_data['GBFS-straightLine'][case_no][0] >= s_data['A*-manhattan'][case_no][0]")
    print("pass: assert s_data['GBFS-squaredEuclid'][case_no][0] >= s_data['A*-manhattan'][case_no][0]")
    print("not pass: assert s_data['GBFS-manhattan'][case_no][0] > s_data['A*-manhattan'][case_no][0] or s_data['GBFS-straightLine'][case_no][0] > s_data['A*-manhattan'][case_no][0] or s_data['GBFS-squaredEuclid'][case_no][0] > s_data['A*-manhattan'][case_no][0]:")
    conclusions.append("Conclusion 4.1 not reached. Greedy Best-First Search found optimal solutions in given testing cases")


  try:
    # Conclusion 4.2
    # GBFS should be faster
    assert r_data['GBFS-manhattan'][1] <= r_data['A*-manhattan'][1]
    assert r_data['GBFS-straightLine'][1] <= r_data['A*-straightLine'][1]
    assert r_data['GBFS-squaredEuclid'][1] <= r_data['A*-squaredEuclid'][1]
    print("pass: assert sum(s_data['GBFS-manhattan'][case_no][1]) <= sum(s_data['A*-manhattan'][case_no][1])")
    print("pass: assert sum(s_data['GBFS-straightLine'][case_no][1]) <= sum(s_data['A*-straightLine'][case_no][1])")
    print("pass: assert sum(s_data['GBFS-squaredEuclid'][case_no][1]) <= sum(s_data['A*-squaredEuclid'][case_no][1])")
    conclusions.append("Conclusion 4.2 reached. Greedy Best-First Search, in general, is faster.")
    completed_conclusion = completed_conclusion + 1
    if GBFS_not_always_faster == True:
      print("not pass: assert s_data['GBFS-manhattan'][case_no][1] <= s_data['A*-manhattan'][case_no][1] and s_data['GBFS-straightLine'][case_no][1] <= s_data['A*-straightLine'][case_no][1] and s_data['GBFS-squaredEuclid'][case_no][1] <= s_data['A*-squaredEuclid'][case_no][1]")
      conclusions.append("Conclusion 4.3 reached. Greedy Best-First Search is not always faster.")
      completed_conclusion = completed_conclusion + 1
    else:
      print("pass: assert s_data['GBFS-manhattan'][case_no][1] <= s_data['A*-manhattan'][case_no][1]")
      print("pass: assert s_data['GBFS-straightLine'][case_no][1] <= s_data['A*-straightLine'][case_no][1]")
      print("pass: assert s_data['GBFS-squaredEuclid'][case_no][1] <= s_data['A*-squaredEuclid'][case_no][1]")
      conclusions.append("Conclusion 4.3 not reached. Greedy Best-First Search performed always faster in given testing cases.")
  except Exception as e:
    print("not pass: assert sum(s_data['GBFS-manhattan'][case_no][1]) <= sum(s_data['A*-manhattan'][case_no][1])")
    print("not pass: assert sum(s_data['GBFS-straightLine'][case_no][1]) <= sum(s_data['A*-straightLine'][case_no][1])")
    print("not pass: assert sum(s_data['GBFS-squaredEuclid'][case_no][1]) <= sum(s_data['A*-squaredEuclid'][case_no][1])")
    conclusions.append("Conclusion 4.2 not reached. Greedy Best-First Search performed not faster in given testing cases.")
    conclusions.append("Conclusion 4.3 reached. Greedy Best-First Search is not always faster.")

  try:
    assert bi_A_not_always_optimal == True
    print("pass: assert s_data['Bi-A*-manhattan'][case_no][0] > s_data['A*-manhattan'][case_no][0]")
    conclusions.append("Conclusion 5.1 reached. Bidirectional A* Search cannot guarantee the optimality.")
    completed_conclusion = completed_conclusion + 1
  except Exception as e:
    print("pass: assert s_data['Bi-A*-manhattan'][case_no][0] >= s_data['A*-manhattan'][case_no][0]")
    print("not pass: assert s_data['Bi-A*-manhattan'][case_no][0] > s_data['A*-manhattan'][case_no][0]")
    conclusions.append("Conclusion 5.1 not reached. Bidirectional A* Search got optimal solution in given testing cases.")
  
  try:
    # Conclusion 5.2
    # Bi-directional A* Search should be faster than corresponding Uni-directional A* Search
    assert r_data['Bi-A*-manhattan'][1] <= r_data['A*-manhattan'][1]
    assert r_data['Bi-A*-straightLine'][1] <= r_data['A*-straightLine'][1]
    assert r_data['Bi-A*-squaredEuclid'][1] <= r_data['A*-squaredEuclid'][1]
    print("pass: assert sum(s_data['Bi-A*-manhattan'][case_no][1]) <= sum(s_data['A*-manhattan'][case_no][1])")
    print("pass: assert sum(s_data['Bi-A*-straightLine'][case_no][1]) <= sum(s_data['A*-straightLine'][case_no][1])")
    print("pass: assert sum(s_data['Bi-A*-squaredEuclid'][case_no][1]) <= sum(s_data['A*-squaredEuclid'][case_no][1])")
    conclusions.append("Conclusion 5.2 reached. Bidirectional A* Search, in general, is faster than A* Search.")
    completed_conclusion = completed_conclusion + 1
    if BiA_not_always_faster == True:
      print("pass: assert s_data['Bi-A*-manhattan'][case_no][1] > s_data['A*-manhattan'][case_no][1] or assert s_data['Bi-A*-straightLine'][case_no][1] > s_data['A*-straightLine'][case_no][1] or assert s_data['Bi-A*-squaredEuclid'][case_no][1] > s_data['A*-squaredEuclid'][case_no][1]")
      conclusions.append("Conclusion 5.3 reached. Bidirectional A* Search is not always faster than A* Search.")
      completed_conclusion = completed_conclusion + 1
    else:
      print("pass: assert s_data['Bi-A*-manhattan'][case_no][1] <= s_data['A*-manhattan'][case_no][1]")
      print("pass: assert s_data['Bi-A*-straightLine'][case_no][1] <= s_data['A*-straightLine'][case_no][1]")
      print("pass: assert s_data['Bi-A*-squaredEuclid'][case_no][1] <= s_data['A*-squaredEuclid'][case_no][1]")
      conclusions.append("Conclusion 5.3 not reached. Bidirectional A* Search is always faster than A* Search.")
  except Exception as e:
    print("not pass: assert sum(s_data['Bi-A*-manhattan'][case_no][1]) <= sum(s_data['A*-manhattan'][case_no][1])")
    print("not pass: assert sum(s_data['Bi-A*-straightLine'][case_no][1]) <= sum(s_data['A*-straightLine'][case_no][1])")
    print("not pass: assert sum(s_data['Bi-A*-squaredEuclid'][case_no][1]) <= sum(s_data['A*-squaredEuclid'][case_no][1])")
    conclusions.append("Conclusion 5.2 not reached. Bidirectional A* Search performed no faster than A* Search in given testing cases.")
    conclusions.append("Conclusion 5.3 reached. Bidirectional A* Search is not always faster than A* Search.")  

  print("\nTesting Results:")
  for c in conclusions:
    print('  ' + c)
  if completed_conclusion == 9:
    print("All conclusions have been reached. Perfect tests.")
  else:
    print("Some Conclusions have not been reached.\nPlease increase the amount of testing cases, or analyze the sample testing log file who has 10000 testing cases.")

  for i in range(3):
    print("\nTable %d:\tAverage\tSteps\t\tNodes\t\tTime" %(i+1))
    output_data = sorted(r_data.items(), key = lambda k: k[1][i], reverse = False)

    for x in output_data:
      if len(x[0]) < 15:
        t = "\t\t"
      else:
        t = "\t"
      print("%s:%s%f\t%f\t%f" % (x[0], t, x[1][0]*1.0/cases, x[1][1]*1.0/cases+1, x[1][2]/cases))
  

if __name__ == "__main__":
  main(sys.argv)
  