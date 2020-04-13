import pandas as pd

# Чтение из файла
data = pd.read_csv('data.csv')
   
# Копируем данные из файла
out = data[data['msisdn_origin'] ==  968247916].copy()
inc = data[data['msisdn_dest'] ==  968247916].copy() 

# Получаем нужные нам данные
out_calls = out['call_duration'].values
sms = out['sms_number'].values
inc_calls = inc['call_duration'].values

    
# Результат
out_final = out_calls * 4
inс_final = (inc_calls - 5) * 1 if  inc_calls >5 else 0
sms_final = (sms - 5) * 1 if sms > 5 else 0
result = out_final + inс_final + sms_final
    
print("Результат: ", end="")
print(*result)