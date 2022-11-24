import calendar


# Create a plain text calendar
def kalendorius(y,m,d,h):
    c = calendar.TextCalendar(calendar.MONDAY)
    str = c.formatmonth(y, m, d, h)
    return print(str)


k=kalendorius(2022,10,0,0)

# # Create an HTML formatted calendar
# hc = calendar.HTMLCalendar(calendar.MONDAY)
# str = hc.formatmonth(2022, 10)
# print(str)
