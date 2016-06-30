from string import Template

import pytest


def test_string_template():
    template = Template("Hello ${name}")

    result = template.substitute({"name": "World"})
    assert "Hello World" == result


def test_string_template_dotted():
    template = Template("Hello ${project.name}")

    with pytest.raises(ValueError):
        template.substitute({"project.name": "World"})


def test_format_dotted():
    template = "Hello {project.name}"

    with pytest.raises(KeyError):
        template.format({"project.name": "World"})
