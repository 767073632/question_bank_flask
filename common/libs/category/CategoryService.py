from flask import jsonify

from common.models.CategoryQuestion import CategoryQuestion


class CategoryService():
    @staticmethod
    def get_json_type12(category):
        category_type1_list = []
        for i in range(category.count()):
            category_type1_list.append(dict(category[i]))
            subclass=[]
            subclass_list = CategoryQuestion.query.filter(CategoryQuestion.parent_category_id==category[i].id)
            for j in range(subclass_list.count()):
                subclass.append(dict(subclass_list[j]))

            category_type1_list[i]['subclass']=subclass
        return category_type1_list

    @staticmethod
    def get_json_type1(category_1):
        category_type1_list = []
        type1_list ={"items":[]}
        type2_list ={"items":[]}
        type3_list ={"items":[]}
        for i in range(category_1.count()):
            if category_1[i].type==1:
                if not type1_list.get('type_id',''):
                    type1_list['type_id']=1
                    type1_list['type_name'] = category_1[i].type_desc
                dict_type1 = dict(category_1[i])
                dict_type1['title'] = dict_type1['name']
                dict_type1.pop('name')
                type1_list["items"].append(dict_type1)

            if category_1[i].type==2:
                if not type2_list.get('type_id',''):
                    type2_list['type_id']=2
                    type2_list['type_name'] = category_1[i].type_desc
                dict_type1 = dict(category_1[i])
                dict_type1['title'] = dict_type1['name']
                dict_type1.pop('name')
                type2_list["items"].append(dict_type1)

            if category_1[i].is_hot==1:
                if not type3_list.get('type_id',''):
                    type3_list['type_id']=3
                    type3_list['type_name'] = '热门'
                dict_type1 = dict(category_1[i])
                dict_type1['title'] = dict_type1['name']
                dict_type1['type'] = 3
                dict_type1.pop('name')
                type3_list["items"].append(dict_type1)

        category_type1_list.append(type1_list)
        category_type1_list.append(type2_list)
        category_type1_list.append(type3_list)
        return category_type1_list

    @staticmethod
    def get_json_type23(category_2):
        category_type23_list = []
        for i in range(category_2.count()):
            dict_typ1 = dict(category_2[i])
            dict_typ1['title'] = dict_typ1['name']
            dict_typ1.pop('name')
            dict_typ1.pop('price')
            dict_typ1.pop('type')
            dict_typ1.pop('is_hot')
            category_type23_list.append(dict_typ1)
            items=[]
            items_list = CategoryQuestion.query.filter(CategoryQuestion.parent_category_id==category_2[i].id)
            for j in range(items_list.count()):
                dict_typ2 = dict(items_list[j])
                dict_typ2['title'] = dict_typ2['name']
                dict_typ2.pop('name')
                dict_typ2.pop('price')
                dict_typ2.pop('type')
                dict_typ2.pop('is_hot')
                items.append(dict_typ2)

            category_type23_list[i]['items']=items
        return category_type23_list

