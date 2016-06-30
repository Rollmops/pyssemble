class DottedTemplate:
    def __init__(self, string):
        self.string = string

    def substitute(self, dictionary):
        substitution = self.string

        transformed_dictionary = DottedTemplate.transform_dictionary(dictionary)

        for key, value in transformed_dictionary.items():
            substitution = substitution.replace(key, str(value))

        return substitution

    @staticmethod
    def transform_dictionary(dictionary):
        transformed_dictionary = {}
        for key in dictionary.keys():
            new_key = "${" + key + "}"
            transformed_dictionary[new_key] = dictionary[key]

        return transformed_dictionary
