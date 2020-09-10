import json
import os

class UserCredentialsCls:

    userCredentials_filePath = "./File/userCredentials.json"  # empty json file is needed at this location

    def checkUsernameExists(self, **kwargs):

        if os.path.isfile(self.userCredentials_filePath) and os.access(self.userCredentials_filePath, os.R_OK):  # check if the file exists

            with open(self.userCredentials_filePath, 'r+') as fp:
                if len(fp.readlines()) != 0:
                    fp.seek(0)
                    dict_userCredentials = json.load(fp)
                else:
                    dict_userCredentials = dict()

            if 'key_username' in kwargs and 'key_pin' in kwargs:  # check if key exists in kwargs

                if kwargs['key_username'] in dict_userCredentials:

                    if kwargs['key_pin'] == dict_userCredentials[kwargs['key_username']]:
                        return "Exist"  # username and pin, both present in file
                    else:
                        return "NotExist"  # username match, pin does not match
                else:
                    return "NotExist"  # username not present in file

            elif 'key_username' in kwargs and 'key_pin' not in kwargs:  # check if key exists in kwargs
                if kwargs['key_username'] in dict_userCredentials:
                    return "Exist"  # only username is present
                else:
                    return "NotExist"  # username is not present
            else:
                return "NotExist" # no arguments passed
        else:
            with open(self.userCredentials_filePath, 'w+') as fp:
                json.dump(dict(), fp) # create empty json file

            return "NotExist"  # file does not exist


    def saveUserCredentials(self, dict):
        with open(self.userCredentials_filePath, 'r+') as fp:
            if len(fp.readlines()) != 0:  # if condition is checked only in r+ mode
                fp.seek(0)
                file_data = json.load(fp)
                file_data.update(dict)
                fp.seek(0)
                json.dump(file_data, fp, indent=4)
            else:
                json.dump(dict, fp, indent=4)

        return "done"
