def callback_enterkey(arg):
    if len(arg[0]) <= 0:
        return
    if type(arg[0][-1]) == str:
        return
    a = eval(' '.join(arg[1]))
    arg[0].clear()
    arg[1].clear()
    arg[0].append(int(a))
    arg[1].append(str(a))


def clear_one(arg):
    if len(arg[0]) <= 0:
        return
    if str(arg[0][-1])[0:-1] == '':
        del arg[0][-1]
        del arg[1][-1]
    elif str(arg[0][-1])[0:-1] != '':
        arg[0][-1] = int(str(arg[0][-1])[0:-1])
        arg[1][-1] = arg[1][-1][0:-1]


def clear_all(arg):
    arg[0].clear()
    arg[1].clear()
