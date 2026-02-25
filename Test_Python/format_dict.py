

# my_nested_dict = {
#     "user1": "No",
#     "user2": {"name": "Bob", "age": 25}
# }
#
# str1:str=""
# for val , key in my_nested_dict.items():
#     str1 = str1+f"**{val}**={key} \n"
#
# print(str1)

my_dict = {'a': 1, 'b': 2, 'c': [1,2,3]}

# Format: "a:1, b:2, c:3"
test1= (f"{key}={value}" for key, value in my_dict.items())
print(type(test1))
formatted_string = "\n".join(f"{key}={value}" for key, value in my_dict.items())
print(formatted_string)

tuple1 = (1,2,3,4)
print("\n".join(str(num) for num in tuple1))