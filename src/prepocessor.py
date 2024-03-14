
import pandas as pd
import re
def preprocess(data): 
    pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s"
    messages = re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)
    df = pd.DataFrame({'user_messages': messages, 'message_date' : dates})
    df['message_date'] = pd.to_datetime(df['message_date'] , format = '%d/%m/%Y, %H:%M - ')
    df.rename(columns = {'message_date' : 'date'} , inplace=True)
    users  = []
    messages = []
    for message in df['user_messages']:
        entry = re.split('([\w\W]+?):\s' , message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns = ['user_messages'], inplace = True)
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['only_date'] = df['date'].dt.date
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name() 
    df['hour'] = df['date'].dt.hour 
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
 

    return df