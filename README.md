# slydb

## 1 Dependency
1. conda运行环境下的配置
- [miniconda安装](https://docs.conda.io/en/latest/miniconda.html)
```conda
conda create -n env_py36 python=3.6
conda activate env_py36
conda install numpy, BTrees
pip install sly
```
2. 用pycharm打开项目，编译器指定conda下env_py36
3. mark slydb folder as source root

## 2 Plan

前期：
- query的实现，
    - 参考tinidb+pandas
    - override自带python method
- B-Tree
- 跑通老师的命令
后期：
- 异常抛出和处理
- typing类型指定
- 代码优化，类和方法的设计，
    - 参考[SQL语法](https://www.w3school.com.cn/sql/index.asp)
    - 参考 python语法
- [代码规范检查](https://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/contents/)



## 3 Notes
### 3.1 pandas_parser
- 前期只需要大致理解complier.py，
- [官方范例](https://sly.readthedocs.io/en/latest/sly.html#writing-a-lexer)
讲的很清晰

**MyLexer:** Break up the input cmd into "tokens".
Strings that correspond to the "base case" symbols used in required grammar.
These are keywords, such as "select" or "create";
punctuation and relation symbols such as "()," ">=<";
and other _database (of columns or tables);

**MyParser:** Execrate tokens.
Consists of a set of functions that can call each other recursively,
to operate on the sequence of tokens:
        @_('statements statements')
        def statements(self, p):
p is a YaccProduction object, {token, matched cmd}
every time use "p.expr", recursively run statement(function) that match its @_().

**举例分析**
select命令执行顺序（最小匹配，递归）
```
pd >> R1 := select(R, (time > 50) and (qty < 30))
NAME COMP NUMBER
NAME COMP NUMBER
"(" expr ")" AND "(" expr ")"
SELECT "(" NAME "," expr ")"
NAME DEFINE expr

pd >> R1 := select(R, ((time > 50) and (qty < 30)) or (time < 10))
NAME COMP NUMBER
NAME COMP NUMBER
"(" expr ")" AND "(" expr ")"
NAME COMP NUMBER
"(" expr ")" OR "(" expr ")"
SELECT "(" NAME "," expr ")"
NAME DEFINE expr
```


### 3.2 previous
- 后期检查里面提到的细致要求
- http://www.7daixie.com/2019120316836054.html

### 3.3 mini-db (python)
- 需要大致理解逻辑和架构，argparser不用看
- NYU CS project **in python**
- Relational DB, cmd parser
- very few watching/star/fork in github
- [source](https://github.com/samarthtambad/mini-db)

### 3.4 dbSystem (java)
- 需要大致理解逻辑和架构，interpret&token不用看
- 题目要求大致相同，Java高级语法用的很好，后期可以考虑（多态/继承/重载）
- Berkeley EECS project **in java**
- Relational DB, cmd parser
- very few watching/star/fork in github
- [source](https://github.com/timkchan/dbSystem)
- [website](https://inst.eecs.berkeley.edu/~cs61b/fa15/hw/proj1/)


### 3.5 tinydb (python)
- 代码很Robust&简短&规范，用于参考
- Document DB(NOSQL), cmd parser
- Super popular in github
- [source]()

### 3.6 python语法
- [概述](https://blog.csdn.net/mk1843109092/article/details/96968465?utm_medium=distribute.pc_relevant.none-task-blog-title-2&spm=1001.2101.3001.4242)
- 多态
- 继承
- [Overriide](https://docs.python.org/zh-cn/3/reference/datamodel.html#special-method-names)
- 装饰器@
- lambda, filter, map

## directory


## 5 Function
### finished
- input
- output
- print eg:R
- project
### 5.1 all
[text.txt]("./data/text.txt")
```txt

// import vertical bar delimited of sales file.
// suppose column headers are saleid|itemid|customerid|storeid|time|qty|pricerange
R := inputfromfile(sales)

// select rows of R whose time > 50 and qty < 30)
R1 := select(R, (time > 50) and (qty < 30))

// select rows of R whose time > 50
R8 := select(R, time > 50)

// if selection filter is string and it’s not any of the column name,
// please add quotation marks
R9 := select(R, pricerange = "outrageous")

// get columns saleid, qty, customerid and pricerange of the rows of R1
R2 := project(R1, saleid, qty, customerid, pricerange)

// get average value of qty of R1
R3 := avg(R1, qty)

// select time, sum group by qty of R1
R4 := sumgroup(R1, time, qty)

// select qty and sum group by time,pricerange of R1
R5 := sumgroup(R1, qty, time, pricerange)

// select qty and avg group by pricerange of R1
R6 := avggroup(R1, qty, pricerange)

// import vertical bar delimited of sales2 file. Suppose column headers are saleid|I|C|S|T|Q|P
S := inputfromfile(sales2)

// T has all the columns of R and S that R_saleid = S_C.
// The column headers are prefaced by the table they came from,
// e.g. R_saleid, R_qty, R_customerid, R_pricerange, S_saleid, S_I, S_C, S_S, S_T, S_Q, S_P
T := join(R, S, R.saleid = S.C)
T1 := join(R1, S, R1.qty <= S.Q)

// sort T1 by S_C
T2 := sort(T1, S_C)

// sort T1 by R1_itemid, S_C (in that order)
T2prime := sort(T1, R1_time, S_C)

// perform the three item moving average of T2
T3 := movavg(T2, R1_qty, 3)

// perform the five item moving sum of T2
T4 := movsum(T2, R1_qty, 5)

// there is no index to use
Q1 := select(S, saleid = 93086)

// create an index on S based on column saleid
Btree(S, saleid)

// this should use the index Btree(S,saleid)
Q2 := select(S, saleid = 93086)

// this should not use an index Btree(S,saleid)
Q3 := select(S, Q > 20)
Hash(S, saleid)

// concatenate the two tables (must have the same schema)
Q5 := concat(Q2, Q3)

// export Q5 to bar file with vertical bar delimiter.
outputtofile(Q5, bar)

```




