class TupleList(list):
    def __init__(self, *args):
        super(TupleList, self).__init__(args)
    
    def __repr__(self):
        return f'<< {str(list(self))} >>'
        
def convert_to_tuples(input_list, element_func=None):
    for i, item in enumerate(input_list):
        if isinstance(item, list):
            input_list[i] = convert_to_tuples(item, element_func)
        elif element_func is not None:
            input_list[i] = element_func(item)
    return TupleList(input_list)

# Define a custom function to perform an operation on list elements (e.g., converting to uppercase)
def custom_operation(element):
    return element.upper()

input_list = ['a', 'b', ['c', 'd', ['i']], 'e', ['f', ['j']], 'g', 'h']

tuple_result = convert_to_tuples(input_list, element_func=custom_operation)

print(tuple_result)

