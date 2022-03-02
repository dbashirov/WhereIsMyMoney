def MonthInWords(currentDate):
    numMonth = int(currentDate.strftime("%m"))
    # print(f'numMonth = {numMonth% 12}, currentDate.strftime("%m") = {currentDate.strftime("%m")}')
    a = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    return a[(numMonth % 12)-1]