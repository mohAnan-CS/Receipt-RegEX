import json
import re


def read_data(file):
    file = open(file, 'r')
    read_list = file.readlines()
    return read_list


def get_receipt_no(read_list):
    pattern = ':'
    arr_split = re.split(pattern, read_list[0])
    receipt_no = arr_split[1].strip(" ")
    return receipt_no.strip("\n")


def get_date(read_list):
    arr_split = re.split(" ", read_list[1])
    date = arr_split[0]
    return date.strip("\n")


def get_time(read_list):
    arr_split = re.split(" ", read_list[1])
    time = arr_split[1] + " " + arr_split[2]
    return time.strip("\n")


def get_items(read_list):
    items = []
    quantity = []
    price = []
    check = False
    for i in read_list:
        split_arr = re.split(":", i)
        index1 = split_arr[0]

        if index1 == "Items count":
            check = False

        if check:
            res = any(chr.isdigit() for chr in split_arr[0])
            if not res:
                items.append(split_arr[0].strip("\n"))
            else:
                split_arr1 = split_arr[0].strip(" ")
                quantity.append(split_arr1[0])
                price.append(split_arr1[5] + split_arr1[6])

        if index1 == "Order No.":
            check = True

    json_arr = create_json_arr(items, quantity, price)
    return json_arr


def create_json_arr(items, quantity, price):
    json_list = []
    count = 0
    for _ in items:
        json_obj = {"item": items[count], "price": price[count], "quantity": quantity[count]}
        json_list.append(json_obj)
    return json_list


def get_total(read_list):
    arr_split = re.split(" ", read_list[13])
    total = arr_split[len(arr_split)-1]
    return total


if __name__ == '__main__':
    data_list = read_data("data")
    receipt_number = get_receipt_no(data_list)
    receipt_date = get_date(data_list)
    receipt_time = get_time(data_list)
    receipt_items = get_items(data_list)
    receipt_total = get_total(data_list)
    receipt = {"Receipt No": receipt_number, "Date": receipt_date, "Receipt Time": receipt_time,
               "Receipt Items": receipt_items, "Receipt Total": receipt_total}
    print(json.dumps(receipt, indent=4))
