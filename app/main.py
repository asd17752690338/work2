from flask import render_template,Flask, jsonify
# from app import app
import re
import os
app = Flask(__name__)


def load_abbreviations():
    # 获取当前目录的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 构建文件路径
    abbreviations_file_path = os.path.join(current_dir, 'data/en-abbreviations.txt')

    abbreviations_dict = {}

    with open(abbreviations_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # 跳过注释行（以 '#' 开头的行）
            if line.startswith('#'):
                continue

            # 使用\s{2,}作为分隔符进行拆分
            parts = re.split(r'\s{2,}', line.strip())

            # 如果有至少两个部分，则将第一个作为键，其余部分组合为值
            if len(parts) > 1:
                abbreviation = parts[0]
                expansions = ' '.join(parts[1:])
                abbreviations_dict[abbreviation] = expansions

    return abbreviations_dict


# 在flask应用初始化时加载缩略语
abbreviations = load_abbreviations()

@app.route('/')
@app.route('/header')
def header():
    top_10_list = list(abbreviations.items())[:10]
    return render_template('header.html',data=top_10_list)

@app.route('/search/<prefix>', methods=['GET'])
@app.route('/search', methods=['GET'])
@app.route('/search/', methods=['GET'])
def search(prefix=""):
    # 检查传入的前缀是否为空
    matched_records = []
    if  prefix:
        matched_records = [
                              (abbreviation, expansions)
                              for abbreviation, expansions in abbreviations.items()
                              if abbreviation.startswith(prefix)
                          ][:10]
    return render_template('search.html',data=matched_records)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
