#!/bin/env python3
"""This module contains the ImageScraper class"""


def _get_opening_root_tag(html_input):
    """Read through html input and return the full html tag (< to >) of the opening tag

    Args:
        html_input (str or bytes): HTML string to read the opening tag from

    Returns:
        str: the full opening tag string, e.g. <div id="ires">

    Raises:
        ValueError: if the provided html does not contain a valid opening tag structure
    """
    # for each character in the html_input, start reading, looking for opening and closing tags at start and end indices
    start_index = None
    end_index = None
    cur_index = 0

    # Make sure that if byte string is passed in, we modify it to be a string
    html_input = html_input.decode() if isinstance(html_input, bytes) else html_input
    for character in html_input:
        if character == "<":
            # If we've already seen an opening tag before seeing the closing tag, bomb out
            if start_index is not None:
                raise ValueError("Parameter html_input does not contain valid HTML - too many opening brackets")
            start_index = cur_index
        elif character == ">":
            # If we haven't seen an opening tag yet, bomb out
            if start_index is None:
                raise ValueError("Parameter html_input does not contain valid HTML - no opening bracket seen")
            end_index = cur_index
            # Break out of the for loop as soon as we find the closing tag to the first tag we found
            break
        cur_index += 1
    # If either an opening tag or a closing tag hasn't been seen,
    #   assume this is just text, and return None since this isn't valid HTML
    if start_index is None or end_index is None:
        return None

    # Return the section of html_input that represents the first valid tag we found
    return html_input[start_index:end_index + 1]


def _get_element_type(tag):
    """This function extracts the type of tag specified in tag

    Args:
        tag (str or bytes): Full valid html tag from < to >

    Returns:
        str: type of HTML tag, e.g. div, p, meta, span, td, etc
    """
    # decode tag parameter if its a bytes object
    tag = tag.decode() if isinstance(tag, bytes) else tag

    # clean up any leading or trailing spaces
    tag = tag.strip()

    # check that we open with an <
    if not tag.startswith("<"):
        raise ValueError("Parameter 'tag' does not start with '<'")

    # Start off the type variable after the open bracket
    tag_type = tag[1:]

    # Clean up leading spaces
    tag_type = tag_type.strip()
    tag_type_iterator_copy = tag_type

    # Find the first index of the next space or the closing brace
    cur_index = 0
    for character in tag_type_iterator_copy:
        if character.isspace() or character == ">":
            tag_type = tag_type[:cur_index]
            break
        cur_index += 1

    return tag_type


def _get_element_id(tag):
    """Extracts the id=* from the tag and returns that as a string

    Args:
        tag (str or bytes): Full valid html tag from < to >

    Returns:
        str or None: ID of the tag parameter, or None if one does not exist
    """
    # decode tag parameter if its a bytes object
    tag = tag.decode() if isinstance(tag, bytes) else tag

    # Find first occurence of "id=" in the tag, and pull out the value
    id_index = tag.find("id=")
    if id_index == -1:
        # id= not found in tag
        return None

    # Determine the quote character used after the id=
    quote_character = tag[id_index + len("id=")]

    # Determine where the ID starts and where it ends, based on the quote character
    start_index = id_index + len("id=") + 1
    end_index = tag.find(quote_character, start_index)

    return tag[start_index:end_index]


def _get_root_contents(html_input):
    """Extracts the contens within the root element and returns them as a string

    Args:
        html_input (str or bytes): html input to extract the root element contents from

    Returns:
         str: contents of the root element
    """
    # Make sure that if byte string is passed in, we modify it to be a string
    html_input = html_input.decode() if isinstance(html_input, bytes) else html_input

    # Trim leading and trailing space from html_input
    html_input = html_input.strip()

    # Get the root tag, so we can extract its contents
    root_tag = _get_opening_root_tag(html_input)
    # pull out the closing tag
    closing_tag = "</{0}>".format(_get_element_type(root_tag))

    contents = ""

    # Check that the root tag doesn't end with />, indicating there are NO contents
    if html_input[len(root_tag)-1:].find(closing_tag) == -1 or root_tag.endswith("/>"):
        # We haven't found a closing tag, so let's return None
        contents = None
    else:
        # Remove the root_opening_tag from the html_input
        html_input = html_input.replace(root_tag, "")

        # Find the next occurence of the closing tag
        closing_index = html_input.find(closing_tag)

        # Only populate contents if a closing tag exists
        if closing_index != -1:
            contents = html_input[:closing_index]

    return contents


def _get_first_root_element(html_input):
    """Gets the first element within html input string

    Args:
        html_input (str or bytes): Html input with which to extract the first element from

    Returns:
        str: html containing the full first element in html_input
    """
    # Make sure that if byte string is passed in, we modify it to be a string
    html_input = html_input.decode() if isinstance(html_input, bytes) else html_input

    root_element = _get_opening_root_tag(html_input)

    if root_element is None:
        root_element = html_input
    else:
        root_contents = _get_root_contents(html_input)
        if root_contents is not None:
            root_element += root_contents
            closing_tag = "</{0}>".format(_get_element_type(root_element))
            root_element += closing_tag

    return root_element


def _get_elements(html_input):
    """Gets the top level elements that are in html_input

    Args:
        html_input (str or bytes): html input to search for top level elements

    Returns:
        list: a list of element html strings
    """
    if html_input is None:
        return ()

    # Make sure that if byte string is passed in, we modify it to be a string
    html_input = html_input.decode() if isinstance(html_input, bytes) else html_input

    # initialize an empty list for the children
    child_elements = []

    # Get the child elements, one by one
    max_iterations = 2000
    iterations = 0
    while len(html_input) > 0 and iterations < max_iterations:
        # it is expected that this produce a ValueError if root_contents is not valid html.
        child = _get_first_root_element(html_input)
        child_elements.append(HtmlElement(child))
        html_input = html_input.replace(child, "")
        iterations += 1
        if iterations == 1000:
            print("Break here")

    return child_elements


def _get_matching_descendants(tag_type=None):
    pass


class HtmlElement(object):
    """Class to track the data associated with an HTML element and its contents and children

    Attributes:
        type (str): the type of element this is, e.g. p, div, td, etc
        id (str): the value of the id= attribute. Defaults to None if nonexistent.
        num_children (int): a count of the number of child elements included in this element
    """
    def __init__(self, html_input):
        open_tag = _get_opening_root_tag(html_input)
        if open_tag is not None:
            self.type = _get_element_type(open_tag)
            self.id = _get_element_id(open_tag)
            self.contents = _get_root_contents(html_input)
            self.children = _get_elements(self.contents)
        else:
            self.type = None
            self.id = None
            self.contents = html_input.decode() if isinstance(html_input, bytes) else html_input
            self.children = []
        self.num_children = len(self.children)

    def get_descendants(self, tag_type=None):
        """Gets descendants of the current HtmlElement that match the type parameter

        Args:
            tag_type (str): Type of tag to look for, e.g. p, div, table, etc. Defaults to None which gets all descendants

        Returns:
            list: list of strings of the elements that match the type flag, all if type is None or not specified
        """
        # recursively go through each child and return the list of children if they match the type field
        pass


class ImageScraper(object):
    """Class to manager caching and optionally downloading images from a Google image search"""
    pass
