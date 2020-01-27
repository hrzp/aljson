from sqlalchemy.orm.collections import InstrumentedList
import json


class BaseMixin:
    caller_stack = list()

    def __init__(self):
        '''
            For better naming convention used both keywords
        '''
        self.to_json = self.to_dict

    def extract_relations(self):
        return self.__mapper__.relationships.keys()

    def extract_columns(self):
        return self.__mapper__.columns.keys()

    def get_columns(self):
        result = dict()
        result['relationships'] = self.extract_relations()
        result['columns'] = self.extract_columns()
        return result

    def convert_columns_to_dict(self, columns):
        result = dict()
        for item in columns:
            result[item] = getattr(self, item)
        return result

    def convert_instrumented_list(self, items):
        result = list()
        for item in items:
            result.append(item.json(self.caller_stack))
        return result

    def detect_class_name(self, item):
        if item.__class__.__name__ == 'InstrumentedList':
            return item[0].__class__.__name__.lower()
        return item.__class__.__name__.lower()

    def convert_relations_to_dict(self, relations):
        result = dict()
        me = self.__class__.__name__.lower()
        self.caller_stack.append(me)

        for relation in relations:
            obj = getattr(self, relation)
            if self.detect_class_name(obj) in self.caller_stack:
                continue
            if type(obj) == InstrumentedList:
                result[relation] = self.convert_instrumented_list(obj)
                continue
            result[relation] = obj.json(self.caller_stack)

        return result

    def to_dict(self, caller_stack=None):
        '''
            Convert a SqlAlchemy query object to a dict
        '''
        self.caller_stack = [] if not caller_stack else caller_stack
        final_obj = dict()
        columns = self.get_columns()
        final_obj.update(self.convert_columns_to_dict(columns['columns']))
        final_obj.update(self.convert_relations_to_dict(
            columns['relationships']))
        return final_obj
