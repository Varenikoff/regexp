import re
import csv

with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = []
    for row in rows:
        full_name = row[0] + ' ' + row[1] + ' ' + row[2]
        split_full_name = full_name.split(' ', maxsplit=2)
        last_name = split_full_name[0].replace(' ', '')
        first_name = split_full_name[1].replace(' ', '')
        surname = split_full_name[2].replace(' ', '')
        list_split_full_name = [last_name, first_name, surname]
        row[0] = last_name
        row[1] = first_name
        row[2] = surname

        pattern = re.compile(r"(\+7|8)?[\s-]*\(?([\d]{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d+)*\s?\(?(доб.)?[\s]?(\d+)?\)?")
        new_phone_number = pattern.sub(r"+7(\2)\3-\4-\5 \6\7", row[5])
        if 'доб' not in new_phone_number:
            new_phone_number = new_phone_number.replace(' ', '')
        row[5] = new_phone_number

        contacts_list.append(row)

list_double_person = []
for i in range(len(contacts_list)-1):
    for j in range(i+1, len(contacts_list)):
        list_person = []
        if (contacts_list[i][0] == contacts_list[j][0]) and (contacts_list[i][1] == contacts_list[j][1]):
            list_person.append(i)
            list_person.append(j)
            list_double_person.append(list_person)

list_val_double_persons = []
for elem in list_double_person:
    list_val_person = []
    for one_double in range(len(list_double_person)):
        list_val_person.append(contacts_list[elem[one_double]])
    list_val_double_persons.append(list_val_person)

list_num_double_persons = []
for one_str in list_double_person:
    for one_string in one_str:
        list_num_double_persons.append(one_string)



list_no_double_persons = []
for one_list in list_val_double_persons:
    list_no_double_person = []
    counter = 0
    for one_person in one_list:
        if counter > 0:
            field_counter = 0
            for one_param in one_person:
                if one_param != '':
                    list_no_double_person[field_counter] = one_param
                field_counter += 1
        else:
            for one_field in one_person:
                list_no_double_person.append(one_field)
        counter += 1
    list_no_double_persons.append(list_no_double_person)

position = 0
for person_number in list_num_double_persons:
    person_count = 0
    for person in contacts_list:
        if person_count == (person_number - position):
            contacts_list.pop(person_count)
            position += 1
        else:
            person_count += 1


for profile in list_no_double_persons:
    contacts_list.append(profile)




with open("phonebook.csv", "w", encoding='utf-8') as output_f:
    datawriter = csv.writer(output_f, delimiter=',')
    datawriter.writerows(contacts_list)