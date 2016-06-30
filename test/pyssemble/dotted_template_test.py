from pyssemble.dotted_template import DottedTemplate


def test_dotted_template():
    template = DottedTemplate("Hello ${project.name}.")

    result = template.substitute({"project.name": "World"})

    assert "Hello World." == result


def test_multiple_dots():
    template = DottedTemplate("Hello ${base.project.name}.")

    result = template.substitute({"base.project.name": "World"})

    assert "Hello World." == result


def test_transform_dictionary():
    my_dict = {"key1": "value", "key1.key2": "value2", "key1.key2.key3": "value3"}
    expected_dict = {"${key1}": "value", "${key1.key2}": "value2", "${key1.key2.key3}": "value3"}

    transformed_dict = DottedTemplate.transform_dictionary(my_dict)

    assert expected_dict == transformed_dict
