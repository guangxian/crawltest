from datetime import datetime, timedelta

# 获取今天的日期和时间
today = datetime.now()
print(f"今天是: {today.strftime('%Y年%m月%d日 %A')}")

# 计算20天后的日期
future_date = today + timedelta(days=31)
print(f"20天后是: {future_date.strftime('%Y年%m月%d日 %A')}")

today = datetime.now()
start = today + timedelta(days=31)
end = today + timedelta(days=31)
# start = datetime.strptime('2025-10-20', '%Y-%m-%d')
# end = datetime.strptime('2025-11-21', '%Y-%m-%d')
tides = []
# 使用列表推导式
dates = [(start + timedelta(days=x)).strftime('%Y-%m-%d')
         for x in range((end - start).days + 1)]

print(dates)