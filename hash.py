import operator


class Hash:
    def __init__(self):
        self.map = {}
        self.records = []

    def search(self, key):
        indexes = self.map.get(key)
        if indexes is not None:
            print('[' + str(key) + ', ' + str(self.records[indexes]) + '] is found successfully')
        else:
            print('[' + str(key) + '] not present')

    def delete(self, key):
        indexes = self.map.get(key)
        if indexes is not None:
            del self.map[key]
            print('[' + str(key) + ', ' + str(self.records[indexes]) + '] is deleted successfully')
        else:
            print('[' + str(key) + '] not present')

    def insert(self, key, value):
        if key in self.map:
            self.map[key].append(value)
        else:
            self.map[key] = [value]

    def range_search(self, notation, cmp_key):
        notation = notation.strip()
        if notation not in [">", "<", ">=", "<=", "==", "!="]:
            raise Exception("Nonsupport notation: {}. Only '>' '<' '>=' '<=' '==' '!='are supported")
        if notation == '==':
            return self.map[cmp_key]
        else:
            comp_func = {
                "<": operator.lt, ">": operator.gt, "=": operator.eq, "!=": operator.ne,
                ">=": operator.ge, "<=": operator.le
            }
            getvalue = []
            func = comp_func[notation]
            for i in self.map:
                if func(i, cmp_key):
                    getvalue.extend(self.map[i])
            return getvalue
