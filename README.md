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
3. 运行complier.py 测试输出

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


## 4 Function
**注意范例命令的调用顺序**
### 4.1 已完成
- input
- output
- print
- select(no index)
- project
- avg

### 4.2 未完成
- join
- sumgroup
- avggroup
- sort
- movavg
- movsum
- BTree
- select(with index)
- HASH
- concat


### 4.3 测试输出
> run compiler.py
```
/Users/nxt/Applications/miniconda3/envs/env_py36/bin/python /Users/nxt/Documents/Project/pandas_parser/compiler.py

[1] pd >> R := inputfromfile(sales)

[2] pd >> R
saleid, itemid, customerid, storeid, time, qty, pricerange
45, item133, customer2, store63, 49, 23, outrageous
658, item75, customer2, store89, 46, 43, outrageous
149, item103, customer2, store23, 67, 2, cheap
398, item82, customer2, store41, 3, 27, outrageous
147, item81, customer2, store4, 92, 11, outrageous
778, item75, customer160, store72, 67, 17, supercheap
829, item112, customer2, store70, 63, 43, supercheap
101, item105, customer2, store9, 74, 28, expensive
940, item62, customer2, store90, 67, 39, outrageous
864, item119, customer12, store38, 67, 49, outrageous
288, item46, customer2, store95, 67, 26, outrageous
875, item83, customer59, store56, 59, 20, outrageous
783, item86, customer180, store29, 67, 46, outrageous
289, item16, customer2, store95, 92, 2, cheap
814, item101, customer2, store45, 49, 41, outrageous
572, item92, customer59, store91, 63, 31, cheap
428, item114, customer51, store29, 42, 15, outrageous

[3] pd >> R1 := select(R, (time > 50) and (qty < 30))

[4] pd >> R1
saleid, itemid, customerid, storeid, time, qty, pricerange
149, item103, customer2, store23, 67, 2, cheap
147, item81, customer2, store4, 92, 11, outrageous
778, item75, customer160, store72, 67, 17, supercheap
101, item105, customer2, store9, 74, 28, expensive
288, item46, customer2, store95, 67, 26, outrageous
875, item83, customer59, store56, 59, 20, outrageous
289, item16, customer2, store95, 92, 2, cheap

[5] pd >> R8 := select(R, time > 50)

[6] pd >> R8
saleid, itemid, customerid, storeid, time, qty, pricerange
149, item103, customer2, store23, 67, 2, cheap
147, item81, customer2, store4, 92, 11, outrageous
778, item75, customer160, store72, 67, 17, supercheap
829, item112, customer2, store70, 63, 43, supercheap
101, item105, customer2, store9, 74, 28, expensive
940, item62, customer2, store90, 67, 39, outrageous
864, item119, customer12, store38, 67, 49, outrageous
288, item46, customer2, store95, 67, 26, outrageous
875, item83, customer59, store56, 59, 20, outrageous
783, item86, customer180, store29, 67, 46, outrageous
289, item16, customer2, store95, 92, 2, cheap
572, item92, customer59, store91, 63, 31, cheap

[7] pd >> R9 := select(R, pricerange = "outrageous")

[8] pd >> R9
saleid, itemid, customerid, storeid, time, qty, pricerange
45, item133, customer2, store63, 49, 23, outrageous
658, item75, customer2, store89, 46, 43, outrageous
398, item82, customer2, store41, 3, 27, outrageous
147, item81, customer2, store4, 92, 11, outrageous
940, item62, customer2, store90, 67, 39, outrageous
864, item119, customer12, store38, 67, 49, outrageous
288, item46, customer2, store95, 67, 26, outrageous
875, item83, customer59, store56, 59, 20, outrageous
783, item86, customer180, store29, 67, 46, outrageous
814, item101, customer2, store45, 49, 41, outrageous
428, item114, customer51, store29, 42, 15, outrageous

[9] pd >> R2 := project(R1, saleid, qty, customerid, pricerange)

[10] pd >> R2
saleid, qty, customerid, pricerange
149, 2, customer2, cheap
147, 11, customer2, outrageous
778, 17, customer160, supercheap
101, 28, customer2, expensive
288, 26, customer2, outrageous
875, 20, customer59, outrageous
289, 2, customer2, cheap

[11] pd >> R3 := avg(R1, qty)

[12] pd >> R3
15.142857142857142

[13] pd >> R4 := sumgroup(R1, time, qty)
Traceback (most recent call last):
  File "/Users/nxt/Documents/Project/pandas_parser/compiler.py", line 230, in <module>
    parser.parse(lexer.tokenize(text))
  File "/Users/nxt/Applications/miniconda3/envs/env_py36/lib/python3.6/site-packages/sly/yacc.py", line 2082, in parse
    value = p.func(self, pslice)
  File "/Users/nxt/Documents/Project/pandas_parser/compiler.py", line 125, in expr
    return self.names[p.NAME0].groupby(p.expr)[p.NAME1].sum()
AttributeError: 'Table' object has no attribute 'groupby'

Process finished with exit code 1
```
