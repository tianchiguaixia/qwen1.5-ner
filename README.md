## qwen1.5-ner
使用Qwen1.5-0.5B-Chat模型进行通用信息抽取任务的微调，旨在：
- 1. 验证生成式方法相较于NER的效果；
- 2. 为新手提供简易的模型微调流程，尽量减少代码量；
- 3. 大模型训练的数据格式处理。

## 数据集选择
任务名称：中文医学命名实体识别V2（CMeEE-V2）
链接：https://tianchi.aliyun.com/dataset/95414
任务内容：将医学文本命名实体划分为九大类，包括：疾病(dis)，临床表现(sym)，药物(dru)，医疗设备(equ)，医疗程序(pro)，身体(bod)，医学检验项目(ite)，微生物类(mic)，科室(dep)。


## 微调框架
https://swift.readthedocs.io/zh-cn/latest/Instruction/LLM%E5%BE%AE%E8%B0%83%E6%96%87%E6%A1%A3.html


## 测试集结果
![image](https://github.com/user-attachments/assets/191a179c-6516-4239-8f92-387eb22ed0fb)

