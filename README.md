# Mini Project by Group 7
Project members:
- Ngo Duy Dat 20225480
- Tran Vuong Hung 20225496
- Nguyen Tran Nghia 20225452
## How to use
-'technical report.pdf': our technical report

-'slide.pptx': our slide

-Folder 'algorithms': our implementation of 6 algorithms

-Folder 'data': where we create and store testcases

-Folder 'notebook': where we draw some graphs and charts to evaluate our algorithms. It should not be run because many names and directories has been changed or removed.

-'main.py': where you can run and test our 6 algorithms.

You can either load input data by function 'load_data_from_input()'  or 'load_data_from_json()' in 'main.py'.
-'load_data_from_input()' allows you to manually input your testcase.You can create a testcase by running the file 'testcase_maker.py' from folder 'data'.
-'load_data_from_json()' allows you to load a testcase from 'data/testcase.json'. To create a new testcase in that json file, run file 'json_testcase_generator.py' from folder 'data'

Note that if you want to test our algorithms, please use 1 of 2 above input functions because these two functions have made small modification to input data. Explicitly, these two input functions add 1 more column (0,0,...,0) to the matrix of amount of products on shelves for describing the amount of products on shelf 0(the door) and our algorithms are all implemented based on that.