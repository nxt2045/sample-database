# sample memory relational database

## 1 how to run
1. conda environment
   - [install miniconda](https://docs.conda.io/en/latest/miniconda.html)
    ```conda
    conda create -n env_py36 python=3.6
    conda activate env_py36
    pip install sly
    ```
2. run test.py for auto-test sample commands
3. run main.py for customize-input commands

## 2 summary
- finish:
 1. ***interpret*** text input to computer language by sly and re package
 2. implement basic query for relational algebra in database
 3. override some of the python method
 4. use ***b-tree*** and hash index to speed up
 5. difference among { =, copy, deepcopy }

- improvement can be done:
 1. try catch
 2. typing check
 3. lock and freeze
 4. lru cache
 5. [code style](https://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/contents/)


## 3 function
### 3.1 supported db query
- input
- output
- print
- BTree
- HASH
- select (with/without index)
- join (with/without index)
- sort (with/without index)
- project
- concat
- avg
- movavg
- movsum
- avggroup
- sumgroup

### 3.2 test output
- run test.py
```

[1] db >> R := inputfromfile(sales1.txt)
 saleid        itemid        customerid    storeid       time          qty           pricerange
 36            14            2             38            49            15            3
 784           90            182           97            46            31            3
[1000 rows and 7 columns]
total time: 0.002730131149291992

[2] db >> S := inputfromfile(sales2.txt)
 saleid        itemid        customerid    storeid       time          qty           pricerange
 3506          13517         16566         45            73            19            4
 78345         10528         4745          20            73            23            1
[100000 rows and 7 columns]
total time: 0.24036812782287598

[3] db >> R1 := select(R, qty < 30)
 saleid        itemid        customerid    storeid       time          qty           pricerange
 36            14            2             38            49            15            3
 801           117           2             43            81            14            5
[585 rows and 7 columns]
total time: 0.00039887428283691406

[4] db >> R3 := avg(R1, qty)
 avg(qty)
 14.805128205128206
[1 rows and 1 columns]
total time: 0.00010895729064941406

[5] db >> R4 := sumgroup(R1, time, qty,pricerange)
 qty           pricerange    sum
 15            3             200
 14            5             789
[124 rows and 3 columns]
total time: 0.0008649826049804688

[6] db >> R6 := avggroup(R1, time, qty,pricerange)
 qty           pricerange    avg
 15            3             66.66666666666667
 14            5             60.69230769230769
[124 rows and 3 columns]
total time: 0.0009751319885253906

[7] db >> T := join(R, S, R.saleid = S.saleid)
 R_saleid      R_itemid      R_customerid  R_storeid     R_time        R_qty         R_pricerange  S_saleid      S_itemid      S_customerid  S_storeid     S_time        S_qty         S_pricerange
 629           134           59            13            98            43            2             629           9494          614           44            73            25            3
 855           132           140           24            67            3             2             855           6016          14782         75            95            36            1
[1000 rows and 14 columns]
total time: 20.543104887008667

[8] db >> T1 := join(R1, S, R1.qty <= S.qty)
 R1_saleid     R1_itemid     R1_customerid R1_storeid    R1_time       R1_qty        R1_pricerange S_saleid      S_itemid      S_customerid  S_storeid     S_time        S_qty         S_pricerange
 36            14            2             38            49            15            3             3506          13517         16566         45            73            19            4
 801           117           2             43            81            14            5             3506          13517         16566         45            73            19            4
[42349722 rows and 14 columns]
total time: 48.66679096221924

[9] db >> T5 := sort(T, S_storeid)
 R_saleid      R_itemid      R_customerid  R_storeid     R_time        R_qty         R_pricerange  S_saleid      S_itemid      S_customerid  S_storeid     S_time        S_qty         S_pricerange
 240           88            59            96            67            25            5             240           8198          8802          1             73            42            1
 608           74            174           41            55            43            1             608           7759          8397          1             27            5             1
[1000 rows and 14 columns]
total time: 0.006424903869628906

[10] db >> T2 := sort(T1, S_storeid)
 R1_saleid     R1_itemid     R1_customerid R1_storeid    R1_time       R1_qty        R1_pricerange S_saleid      S_itemid      S_customerid  S_storeid     S_time        S_qty         S_pricerange
 36            14            2             38            49            15            3             58541         8123          5746          1             72            48            1
 801           117           2             43            81            14            5             58541         8123          5746          1             72            48            1
[42349722 rows and 14 columns]
total time: 212.20054697990417

[11] db >> T3 := movavg(T2, R1_qty, 3)
 R1_saleid     R1_itemid     R1_customerid R1_storeid    R1_time       movavg(R1_qty)R1_pricerange S_saleid      S_itemid      S_customerid  S_storeid     S_time        S_qty         S_pricerange
 36            14            2             38            49            15.0          3             58541         8123          5746          1             72            48            1
 801           117           2             43            81            14.5          5             58541         8123          5746          1             72            48            1
[42349722 rows and 14 columns]
total time: 535.496787071228

[12] db >> T4 := movsum(T, R_qty, 5)
 R_saleid      R_itemid      R_customerid  R_storeid     R_time        movavg(R_qty) R_pricerange  S_saleid      S_itemid      S_customerid  S_storeid     S_time        S_qty         S_pricerange
 629           134           59            13            98            43            2             629           9494          614           44            73            25            3
 855           132           140           24            67            46            2             855           6016          14782         75            95            36            1
[1000 rows and 14 columns]
total time: 0.019697904586791992

[13] db >> Q1 := select(S, saleid = 93086)
 saleid        itemid        customerid    storeid       time          qty           pricerange
 93086         8436          2718          30            73            50            1
[1 rows and 7 columns]
total time: 0.05850100517272949

[14] db >> Btree(S, saleid)
total time: 0.3779318332672119

[15] db >> Q2 := select(S, saleid = 93086)
 saleid        itemid        customerid    storeid       time          qty           pricerange
 93086         8436          2718          30            73            50            1
[1 rows and 7 columns]
total time: 0.00020313262939453125

[16] db >> Q3 := select(S, qty > 20)
 saleid        itemid        customerid    storeid       time          qty           pricerange
 78345         10528         4745          20            73            23            1
 79991         6715          707           75            41            34            4
[60108 rows and 7 columns]
total time: 0.03265190124511719

[17] db >> Hash(S, saleid)
total time: 0.0852210521697998

[18] db >> Q5 := concat(Q2, Q3)
 saleid        itemid        customerid    storeid       time          qty           pricerange
 93086         8436          2718          30            73            50            1
 78345         10528         4745          20            73            23            1
[60109 rows and 7 columns]
total time: 0.0038912296295166016

[19] db >> outputtofile(Q5, bar)
total time: 0.08197569847106934
```

### 3.3 command format
```
The possible commands are all specified in the assignment and my subsequent announcement. If still unclear, here's a complete list. Below: COP means a comparison operation given in the assignment. R, S and T represent any table, C1 and C2 for a single column, Clist for a non-empty comma separated list of columns. In operations with a single input table (e.g., "select"), column names are always assumed to be from that table. In operations of two input tables (like "join"), column names are always prefixed with the table name they belong to, like, R.C1, S.C2. I also specify the requirement on the order of the rows after each operation.

R := inputfromfile(filename) // import vertical bar delimited file, first line has column headers (and each column is of type int). Create table R. The order of the rows in R is exactly like what is given in the file.

R := select(S, CONDITION), where CONDITION takes the form of: C1 COP CONSTANT or C1 COP C2. The order of the rows in R is the same as those in S (of course, some of the rows are not selected and hence dropped).

R := project(S, Clist) , where Clist is a list of comma separated columns. The order of the rows of R is the same as that of S.

R := sum(S, C1) : this is for "select sum(C1) from S;". This gives a single row table.

R := avg(S, C1) : this is for "select avg(C1) from S;". This gives a single row table.

R := sumgroup(S, C1, Clist) ,  this is for "select Clist, sum(C1) from S group by Clist". The order of the rows in R can be arbitrary.

R := avggroup(S, C1, Clist) ,  this is for "select Clist, avg(C1) from S group by Clist". The order of the rows in R can be arbitrary.

T := join(R, S, JOIN_CONDITION) , where JOIN_CONDITION is of the form R.C1 COP S.C2, where R.C1 is a column of R and S.C2 is a column of S. (Note that columns in join condition are alwasy prefixed with the table they belong to.) The order of the rows in R can be arbitrary.

R := sort(S, C1), this is to sort S by C1 in increasing order (you may assume always a single column sort: this is another simplification)

R := movavg(S, C1, k), this is to perform the k item moving average of S on column C1 (single column). The order of the rows in R is the same as that in S.

R := movsum(S, C1, k), this is to perform the k item moving sum of S on column C1 (single column). The order of the rows in R is the same as that in S.

Btree(R, C1), this is to create a B+tree index on R based on column C1.

Hash(R, C1), this is to create a hash structure on on R based on column C1.

T := concat(R, S), this is to concatenate the two tables R and S (R goes first, and S follows).

outputtofile(R, bar), this is to print out table R to standardout (in this case, "bar" is simply ingored). The printed rows should be in the same order as that in R.
```




## 4 reference
### 4.1 pandas_parser
- [official tutorial](https://sly.readthedocs.io/en/latest/sly.html#writing-a-lexer)

- order for select（最小匹配，递归）
    ```
    db >> R1 := select(R, (time > 50) and (qty < 30))
    NAME COMP NUMBER
    NAME COMP NUMBER
    "(" expr ")" AND "(" expr ")"
    SELECT "(" NAME "," expr ")"
    NAME DEFINE expr
    ```
    ```
    db >> R1 := select(R, ((time > 50) and (qty < 30)) or (time < 10))
    NAME COMP NUMBER
    NAME COMP NUMBER
    "(" expr ")" AND "(" expr ")"
    NAME COMP NUMBER
    "(" expr ")" OR "(" expr ")"
    SELECT "(" NAME "," expr ")"
    NAME DEFINE expr
    ```

### 4.2 tiny-db (python)
- document db, command interpreter
- query lru cache, json/memory storage,

### 4.3 mini-db (python)
- relational db, command interpreter
- [github](https://github.com/samarthtambad/mini-db)

### 4.4 dbsystem (java)
- relational db, command interpreter
- 多态/继承/overwrite
- [source](https://github.com/timkchan/dbSystem)
- [github](https://inst.eecs.berkeley.edu/~cs61b/fa15/hw/proj1/)
