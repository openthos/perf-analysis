### 来源：
* [知乎](https://www.zhihu.com/question/25483589)  
* [阮一峰_asm.js和Emscripten入门教程](http://www.ruanyifeng.com/blog/2017/09/asmjs_emscripten.html)  
* 《JavaScript高级程序设计》

### asm.js和Emscriten
* asm.js  
  是由Mozilla提出的一个基于JS的语法标准，主要是为了解决JS引擎的执行效率问题
* Emscripten  
  是Mozilla的一个实验性项目，目的是把C/C++开发的应用编译成JS或HTML5的应用  
  emcc是Emscripten的编译器前端

### JavaScript
* JavaScript = ECMAscript + DOM + BOM
* ECMAscript语法
  1. 区分大小写。
  2. 标识符以字母，下划线或美元符号开头。
  3. 注释与C语言完全相同。单行(//)，多行`(/* */)`。
  4. 严格模式("use strict";)
  5. 语句建议以分号结尾，用好代码块。
* 关系字和保留字
* 变量定义 var
* 数据类型 (5种基本数据类型和1种复杂数据类型)
  1. 基本数据类型：Undefined, Boolean, Number, String, Null
  2. 复杂数据类型：Object
  3. 不支持自定义数据类型
  4. typeof操作符检测数据类型
  5. 
