def write_new_sum(sum_in_usd):
    sum_file = open("sum", 'w+')
    sum_file.write(str(sum_in_usd))
    sum_file.close()


def get_sum():
    import os

    if os.path.exists('sum'):
        sum_file = open("sum", 'r+')
        sum_string = sum_file.readline()
        sum_file.close()

        if len(sum_string) == 0:
            return 0
        return int(sum_string)
    else:
        return 0
