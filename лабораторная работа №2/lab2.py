import pandas as pd

# Getting started
text = []
with open('nfcapd.txt', 'r', encoding='utf_8') as f:
    text = f.readlines()

spaces = [' ' * n for n in range(20, 2, -1)]

for i in range(len(text)):
    text[i] = text[i].replace('->', '')

words = ['INVALID', 'XEvent', 'Ignore']
for word in words:
    for i in range(len(text)):
        text[i] = text[i].replace(word, ' ' + word + ' ')

for space in spaces:
    for i in range(len(text)):
        text[i] = text[i].replace(space, '  ')

for i in range(len(text)):
    text[i] = text[i].replace('  ', ',')

with open('new_nfcapd.txt', 'w', encoding='utf_8') as f:
    f.writelines(text)

# Reading data
data = pd.read_csv('new_nfcapd.txt', sep=',')

total_traffic = data[(data['Src IP Addr:Port'].str.contains('192.168.250.1')) | (
    data['Dst IP Addr:Port'].str.contains('192.168.250.1'))].reset_index(drop=True).copy()
total_traffic['Date first seen'] = total_traffic['Date first seen'].apply(pd.to_datetime).copy()
total_traffic['In Byte'] = total_traffic['In Byte'].apply(
    lambda x: float(x) if x[-1] != 'M' else float(x[:-1]) * 1024 * 1024).copy()
result = sum(total_traffic['In Byte'].values)
result = round((result / 1024), 2)
print(f'Итоговый объём трафика: {result}Кб')

# Graphics
import matplotlib.pyplot as plt

total_traffic['Date first seen'] = total_traffic['Date first seen'].apply(lambda x: str(x)[:str(x).find('.')]).copy()
total_traffic['Date first seen'] = total_traffic['Date first seen'].apply(pd.to_datetime).copy()
total_traffic['Date first seen'] = total_traffic['Date first seen'].apply(lambda x: str(x)[:-3]).copy()
total_traffic['Date first seen'] = total_traffic['Date first seen'].apply(pd.to_datetime).copy()

traffic_after_group = (total_traffic.groupby('Date first seen').aggregate(sum)).copy()

plt.figure(figsize=(15, 10))
plt.title('Minutes')
plt.plot(traffic_after_group.index, traffic_after_group['In Byte'].values)

# Showing graphics
plt.show()

#Calculating
price = 0
price_500 = 0.5

while result > 0:
    if result >= 500.0:
        price += price_500 * 500
    else:
        price += result * price_500

    price_500 += 0.5
    result -= 500

price = round(price, 2)

print(f'Итоговый результат: {price}')
