## 任务简介
使用Qwen1.5-0.5B-Chat模型进行通用信息抽取任务的微调，旨在：
- 验证生成式方法相较于抽取式NER的效果；
- 为新手提供简易的模型微调流程，尽量减少代码量；
- 大模型训练的数据格式处理。

## 数据集选择
- 任务名称：中文医学命名实体识别V2（CMeEE-V2）
- 链接：https://tianchi.aliyun.com/dataset/95414
- 任务内容：将医学文本命名实体划分为九大类，包括：疾病(dis)，临床表现(sym)，药物(dru)，医疗设备(equ)，医疗程序(pro)，身体(bod)，医学检验项目(ite)，微生物类(mic)，科室(dep)。


## 微调框架
https://swift.readthedocs.io/zh-cn/latest/Instruction/LLM%E5%BE%AE%E8%B0%83%E6%96%87%E6%A1%A3.html


## 排行榜
![image](https://github.com/user-attachments/assets/02e9616f-11ef-49ad-ba2c-5ad6c584b61d)

## 自己微调结果
![image](https://github.com/user-attachments/assets/191a179c-6516-4239-8f92-387eb22ed0fb)

## 结论
1.生成式相比抽取式ner，zero-shot的效果更好。
2.微调以后的抽取式ner效果更强，但是两者之间差距正在缩小。
