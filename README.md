# find-Chinese-medical-words
从网上抓取的医疗语料中，以一种改进的无监督方法寻找语料库存在的词；<br>
主要方法利用互信息熵，正向最大匹配，搜索引擎进行迭代来找词；<br>
语料库不限领域，本实验是以医疗领域的文本；<br>

环境
=
python2/3<br>
requests<br>
lxml<br>

方法
=
step1:统计语料库中出现单字，双字的频率，前后链接的字相关信息；<br>

step2:对统计出的单字和双字的结果，使用互信熵，选择大于阈值K=10.8的词加入词库，作为初始词库；<bar>
  
step3:有了初始词库，使用正向最大匹配，对语料库进行切分，对切分出来的字串按频率排序输出并记下数量seg_num；<br>

step4:对切分产生的字串按频率排序，前H=2000的字串进行搜索引擎（百度）,若字串是“百度百科”收录词条，将该字串作为词加入词库，或者在搜索页面的文本中出现的次数超过阈值R=60,也将该字串作为词加入词库；<br>

step5:更新词库后，重复step3，step4进行迭代，,当searh_num=0时，结束迭代；当seg_num小于设定的Y=5000,进行最后一次step4，并H设定为H=seg_num，执行完后结束迭代，最后词库就是本程序所找的词；<br>

方法流程图
=
![image](https://github.com/cjymz886/find-Chinese-medical-words/tree/master/images/process.jpg)<br>

算法公式
=


运行
=
python medfw.py<br>
其中涉及的参数可根据实际环境进行调整<br>


结果
=
最终输出的词库在./data/dict.txt文件中；<br>
./data目录中是语料库和程序产生的中间数据

结果样例
=
惶惶	org<br>
爷爷	org<br>
曼佗	org<br>
垮垮	org<br>
萧轼	org<br>
艇舰	org<br>
蝰蛇	org<br>
攸琐	org<br>
咔嚓	org<br>
喀嚓	org<br>
铒翠	org<br>
诚挚	org<br>
迪厅	org<br>
不足	iter_0<br>
知情同意书	iter_0<br>
运动	iter_0<br>
状态	iter_0<br>
瘢痕	iter_0<br>
心悸	iter_0<br>
步态	iter_0<br>
祸首	iter_0<br>
照相	iter_0<br>
形成	iter_0<br>
面容	iter_0<br>
先天	iter_0<br>
动作	iter_0<br>
由于	iter_0<br>
价格	iter_0<br>
行为	iter_0<br>
淋病	iter_0<br>
包括	iter_0<br>
栓塞	iter_0<br>
球感	iter_0<br>
