import json
import logging
import re


class KWscript:
    def __init__(self):
        self.headers_list = {"first_name": 0,
                             "middle_name": 0,
                             "last_name": 0,
                             "office_name": 0,
                             "title": 0,
                             "description": 0,
                             "languages": 0,
                             "image_url": 0,
                             "address": 0,
                             "city": 0,
                             "state": 0,
                             "country": 0,
                             "zipcode": 0,
                             "office_phone_numbers": 0,
                             "agent_phone_numbers": 0,
                             "email": 0,
                             "website": 0,
                             "social": 0,
                             "profile_url": 0}

        self.file_list = []
        self.issues_list = []
        self.line_number = 0
        path = input("enter the input file :")
        self.read_file(path)

    def read_file(self, path):
        try:
            file_name = path
            with open(path, 'r') as f:
                for jsonObj in f:
                    self.file_list.append(json.loads(jsonObj))
            file_extention = file_name.split(".")[-1]
            if file_extention != "json":
                value = {file_extention: "file formate is not valid or correct"}
                self.issues_list.append(value)
            self.pre_validation()

        except:
            logging.warning("there has been a error in loading file")
            self.__init__()

    def is_dict(self, key, value):
        if type(value) != type(dict()):
            error = {self.line_number: f"{key} not in proper format "}
            self.issues_list.append(error)

    def is_str(self, key, value):
        if type(value) != type(str()):
            error = {self.line_number: f"{key} not in proper format "}
            self.issues_list.append(error)

    def is_list(self, key, value):
        if type(value) != type(list()):
            error = {self.line_number: f"{key} not in proper format "}
            self.issues_list.append(error)

    def phone_number_validation(self, key, value):
        for i in value:
            if re.search("[A-Za-z]", i):
                error = {self.line_number: f"{key} contains alphabets "}
                self.issues_list.append(error)

    def email_validation(self, key, value):
        if value!="":
            pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
            if re.match(pat, value):
                pass
            else:
                error = {self.line_number: f"{key} is invalid email "}
                self.issues_list.append(error)

    def pre_validation(self):
        for file in self.file_list:
            self.line_number += 1
            for key in file.keys():
                if key not in self.headers_list.keys():
                    value = {self.line_number: f"{key} is not valid or correct header"}
                    self.issues_list.append(value)
                if file.get(key) == "":
                    try:
                        value = {key: self.headers_list[key] + 1}
                        self.headers_list.update(value)
                    except:
                        pass
                elif type(file.get(key)) == type(list()):
                    if not file.get(key):
                        value = {key: self.headers_list[key] + 1}
                        self.headers_list.update(value)
                elif type(file.get(key)) == type(dict()):
                    if not file.get(key):
                        value = {key: self.headers_list[key] + 1}
                        self.headers_list.update(value)
                common_errors = ["\n", "\r", "\t"]
                for error in common_errors:
                    if error in file.get(key):
                        value = {self.line_number: f"contains {error} in {key} "}
                        self.issues_list.append(value)
                pa=file.get(key)
                if type(pa)==str:
                    if re.match(r"^\s+",pa):
                        error = {self.line_number: f"{key} contains extra space in front "}
                        self.issues_list.append(error)
                    if re.match(r"\s{2,}",pa):
                        error = {self.line_number: f"{key} contains extra spaces "}
                        self.issues_list.append(error)
                if type(file.get(key)) == type(None):
                    value = {self.line_number: f"contains None in {key} "}
                    self.issues_list.append(value)
                if key == 'social':
                    value1 = file.get(key)
                    self.is_dict(key, value1)
                elif key == 'agent_phone_numbers' or key == 'office_phone_numbers' or key == 'languages':
                    value1 = file.get(key)
                    self.is_list(key, value1)
                else:
                    value1 = file.get(key)
                    self.is_str(key, value1)
                if key == 'agent_phone_numbers' or key == 'office_phone_numbers':
                    value1 = file.get(key)
                    self.phone_number_validation(key, value1)
                if key == 'email':
                    value1 = file.get(key)
                    self.email_validation(key, value1)

        value = {"Empty Field counts": self.headers_list}
        self.issues_list.append(value)
        logging.warning(self.issues_list)
        for i in self.issues_list:
            with open("issues.log", 'a') as f:
                f.write(json.dumps(i, ) + '\n')

        self.__init__()


KWscript()
