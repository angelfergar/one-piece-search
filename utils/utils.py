class Util():

    def verify_list_length(self, expected_list, actual_list):
        expected_length = len(expected_list)
        actual_length = len(actual_list)
        if expected_length == actual_length:
            return True
        else:
            print("The list's length is not the same as the expected")
            return False