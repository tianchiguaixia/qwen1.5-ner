## 数据处理

import json

# Load the data
file_path = 'CMeEE-V2_train.json'
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Define the entity type mappings
entity_type_mapping = {
    "dis": "疾病",
    "sym": "临床表现",
    "pro": "医疗程序",
    "equ": "医疗设备",
    "dru": "药物",
    "ite": "医学检验项目",
    "bod": "身体",
    "dep": "科室",
    "mic": "微生物类"
}


# Transform the data to the specified format without backslashes
transformed_data = []
for item in data:
    query = item['text']
    response_entities = [{"type": entity_type_mapping[entity["type"]], "entity": entity["entity"]} for entity in item["entities"]]
    transformed_item = {
        "query": "你是一名医学信息抽取的专家，根据输入的文本，抽取出如下实体：疾病, 临床表现, 医疗程序, 医疗设备, 药物, 医学检验项目, 身体, 科室, 微生物类。如果存在对应的实体就抽取，不存在就不抽取。输入的文本："+query,
        "response": str(response_entities)
    }
    transformed_data.append(transformed_item)

# Save the transformed data in one line format
output_path = 'CMeEE-V2_train_transformed.json'
with open(output_path, 'w', encoding='utf-8') as file:
    for item in transformed_data:
        json.dump(item, file, ensure_ascii=False)
        file.write('\n')



## 转换为标准格式
import json

input_file = 'CMeEE-V2_train_transformed.json'
output_file = 'CMeEE-V2_train_transformed_fixed.json'

# Read the file and parse each JSON object
with open(input_file, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Convert each line to a JSON object
json_objects = [json.loads(line) for line in lines]

# Save as a JSON array
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(json_objects, file, ensure_ascii=False, indent=4)


## 模型训练
!CUDA_VISIBLE_DEVICES=0 swift sft \
    --model_id_or_path qwen/Qwen2-7B \
    --dataset CMeEE-V2_train_transformed_fixed.json \
    --output_dir output \
    --num_train_epochs 10 \
    --do_sample False


## 模型推理
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

from swift.llm import (
    get_model_tokenizer, get_template, inference, ModelType, get_default_template_type
)
from swift.tuners import Swift

ckpt_dir = './checkpoint-12370'
model_type = ModelType.qwen2_7b
template_type = get_default_template_type(model_type)

model, tokenizer = get_model_tokenizer(model_type, model_kwargs={'device_map': 'auto'})

model = Swift.from_pretrained(model, ckpt_dir, inference_mode=True)
template = get_template(template_type, tokenizer)

query = '''你是一名医学信息抽取的专家，根据输入的文本，抽取出如下实体：疾病, 临床表现, 医疗程序, 医疗设备, 药物, 医学检验项目, 身体, 科室, 微生物类。如果存在对应的实体就抽取，不存在就不抽取。输入的文本：
（5）房室结消融和起搏器植入作为反复发作或难治性心房内折返性心动过速的替代疗法。'''
response, history = inference(model, template, query)
print(f'response: {response}')



## 批量验证
import json

# 读取JSON文件
with open('CMeEE-V2_test.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 定义类型映射
type_mapping = {
    "疾病": "dis",
    "临床表现": "sym",
    "医疗程序": "pro",
    "医疗设备": "equ",
    "药物": "dru",
    "医学检验项目": "ite",
    "身体": "bod",
    "科室": "dep",
    "微生物类": "mic"
}

# 定义反向映射
reverse_type_mapping = {v: k for k, v in type_mapping.items()}

# 函数：转换类型并计算索引
# 处理数据
total=0

process_data = []
for item in data:
    try:
        text = item['text']
        prompt="你是一名医学信息抽取的专家，根据输入的文本，抽取出如下实体：疾病, 临床表现, 医疗程序, 医疗设备, 药物, 医学检验项目, 身体, 科室, 微生物类。如果存在对应的实体就抽取，不存在就不抽取。输入的文本："
        query=prompt+text
        response, history = inference(model, template, query)
        response=eval(response)

        new_entities = []
        for entity in response:
            entity_type = type_mapping[entity['type']]
            entity_text = entity['entity']
            start_idx = text.find(entity_text)
            end_idx = start_idx + len(entity_text)
            new_entities.append({
                'start_idx': start_idx,
                'end_idx': end_idx,
                'type': entity_type,
                'entity': entity_text
            })
        process_data.append({
            'text': text,
            'entities': new_entities
        })
    except:
        process_data.append({
            'text': text,
            'entities': []
        })

    total=total+1
    print("total",total)

# 保存到新的JSON文件
with open('processed_data.json', 'w', encoding='utf-8') as file:
    json.dump(process_data, file, ensure_ascii=False, indent=4)

print("数据处理完成并保存到processed_data.json")






