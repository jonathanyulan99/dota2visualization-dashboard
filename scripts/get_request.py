import requests

url = 'https://www.w3schools.com/python/demopage.htm'
x_list = list() 
x_string = str()
x = requests.get(url)
y = requests.get(url)
z = requests.get(url)

x1 = x.text
y1 = y.text
z1 = z.text

x_list += x1
x_list += y1
x_list += z1

x_string +=x1
x_string +=y1
x_string +=z1

print(type(x_string),type(x_list),x_string,x_list)
