class Util():

    @staticmethod
    def verify_list_length(expected_list, actual_list):
        if len(expected_list) != len(actual_list):
            print("The list's length is not the same as the expected")
            return False
        return False

    @staticmethod
    def verify_text_contains(actual_text, expected_text):
        if actual_text.lower() in expected_text.lower():
            return True
        print("Text does not contain the expected content")
        return False
