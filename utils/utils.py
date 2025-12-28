class Util():

    @staticmethod
    def verify_list_length(self, expected_list, actual_list):
        expected_length = len(expected_list)
        actual_length = len(actual_list)
        if expected_length == actual_length:
            return True
        else:
            print("The list's length is not the same as the expected")
            return False

    @staticmethod
    def verify_text_contains(self, actual_text, expected_text):
        print(actual_text)
        print(expected_text)
        if actual_text.lower() in expected_text.lower():
            return True
        else:
            print("Text does not contain the expected content")
            return False