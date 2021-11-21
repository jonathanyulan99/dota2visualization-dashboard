import re
txt1 = 'c:\repo\PROJECT_CTP\players\92080451.csv'

txt1_split = txt1.split('/')
for element in range(len(txt1_split)):
    print(txt1_split[element])


x1 = txt1.split('/')
for element in x1:
    if element.isdigit()==True:
        print("it's true")
    if re.match( '^[-+]?(([0-9]+([.][0-9]*)?)|(([0-9]*[.])?[0-9]+))$', element):
        print("It's An Integer")
    else:
        print("It's Not An Integer")

print(type(x1))