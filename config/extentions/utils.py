from time import time
from . import jalili
from django.utils import timezone

def jalali_converter(time):

    jalali_months_list = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
    time = timezone.localtime(time)

    time_to_str = "{} {} {}".format(time.year, time.month, time.day)
    time_to_tuple = jalili.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)


    for index, month in enumerate(jalali_months_list):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break


    output = "{} {} {} ساعت {}:{}".format(
        time_to_list[2],
        time_to_list[1],
        time_to_list[0],
        time.hour,
        time.minute
    )

    return persian_numbers_converter(output)





def persian_numbers_converter(input):

    numbers_dict = {
        '0' : "۰",
        '1' : "۱",
        '2' : "۲",
        '3' : "۳",
        '4' : "۴",
        '5' : "۵",
        '6' : "۶",
        '7' : "۷",
        '8' : "۸",
        '9' : "۹"
    }


    for e, p in numbers_dict.items():
        input = input.replace(e, p)
    
    return input