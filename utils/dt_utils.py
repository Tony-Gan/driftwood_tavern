import os
import sys
import json


class DTUtils:
    @staticmethod
    def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    @staticmethod
    def read_class_features(cl):
        path = DTUtils.resource_path('resources/data/class_features.json')
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        data = data[cl]

        organized = {}
        for level, features in data.items():
            organized[level] = []
            for feature in features:
                organized[level].append({
                    "中文名称": feature["c_name"],
                    "英文名称": feature["e_name"],
                    "描述": feature["description"],
                    "来源": feature["source"],
                    "子职": "无" if not feature["subclass"] else feature["subclass"],
                    "显示类型": feature["display"]
                })

        return organized
    
    @staticmethod
    def read_class_subclass(cl):
        path = DTUtils.resource_path('resources/data/class_subclass.json')
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        data = data[cl]

        organized = {}
        for name, source in data.items():
            organized[name] = source

        return organized
