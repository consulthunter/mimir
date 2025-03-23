import chardet
from typing import List
from tree_sitter import Language, Parser
from tree_sitter import Tree


class BaseParser:

    def __init__(self, supported_lang):
        self.language = Language(supported_lang)
        self.parser = Parser(self.language)
        self.content = None
        self.encoding = None

    def parse_file(self, file):
        """
        Parses a source file and extract
        metadata of all the classes and methods defined
        """
        # Detect file encoding
        with open(file, "rb") as rawdata:
            result = chardet.detect(rawdata.read(10000))
        self.encoding = result['encoding']

        try:
            with open(file, "r", encoding=self.encoding) as content_file:
                content = content_file.read()
                self.content = content
        except (UnicodeDecodeError, IOError):
            return list()

        tree = self.parser.parse(bytes(content, self.encoding)) # Tree
        return tree

    @staticmethod
    def get_class_metadata(class_node, blob: str):
        """
        Extract class-level metadata
        """
        pass

    def get_method_names(self, file):
        """
        Extract the list of method names defined in a file
        """
        pass

    @staticmethod
    def get_function_name(function_node, blob: str):
        """
        Extract method name
        """
        pass

    @staticmethod
    def match_from_span(node, blob: str) -> str:
        """
        Extract the source code associated with a node of the tree
        """
        line_start = node.start_point[0]
        line_end = node.end_point[0]
        char_start = node.start_point[1]
        char_end = node.end_point[1]
        lines = blob.split("\n")
        if line_start != line_end:
            return "\n".join(
                [lines[line_start][char_start:]]
                + lines[line_start + 1 : line_end]
                + [lines[line_end][:char_end]]
            )
        else:
            return lines[line_start][char_start:char_end]

    @staticmethod
    def traverse_type(node, results: List, kind: str) -> None:
        """
        Traverses nodes of given type and save in results
        """
        if node.type == kind:
            results.append(node)
        if not node.children:
            return
        for n in node.children:
            TestifyParser.traverse_type(n, results, kind)

    @staticmethod
    def is_method_body_empty(node):
        """
        Check if the body of a method is empty
        """
        pass

    @staticmethod
    def children_of_type(node, types):
        """
        Return children of node of type belonging to types

        Parameters
        ----------
        node : tree_sitter.Node
            node whose children are to be searched
        types : str/tuple
            single or tuple of node types to filter

        Return
        ------
        result : list[Node]
            list of nodes of type in types
        """
        if isinstance(types, str):
            return TestifyParser.children_of_type(node, (types,))
        return [child for child in node.children if child.type in types]
