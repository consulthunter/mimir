import tree_sitter_java as ts_java
from tree_sitter import Node
from typing import Generator

from mimir.models.class_model import ClassModel
from mimir.models.method_model import MethodModel
from mimir.parsers.base_parser import BaseParser

class JavaParser(BaseParser):

    def __init__(self, project, file_path):
        self.file_path = str(file_path)
        self.project = project
        super().__init__(ts_java.language())
        self.tree = self.parse_file(file_path)
        self.data = ClassModel("java")

        self.current_method_node: Node = None
        self.current_method_info: MethodModel = None

        for node in self.traverse_tree():
            self.process_node(node)

        # check to add last method
        need_to_add_last_method_info = True
        for method in self.data.methods:
            if method.name == self.current_method_info.name:
                need_to_add_last_method_info = False
                break

        if need_to_add_last_method_info and self.current_method_info is not None:
            self.data.methods.append(self.current_method_info)

        self.project.data[self.file_path] = self.data.to_dict()


    def traverse_tree(self) -> Generator[Node, None, None]:
        try:
            cursor = self.tree.walk()
            visited_children = False
            while True:
                if not visited_children:
                    yield cursor.node
                    if not cursor.goto_first_child():
                        visited_children = True
                elif cursor.goto_next_sibling():
                    visited_children = False
                elif not cursor.goto_parent():
                    break
        except Exception as e:
            self.project.logger.log_info(self.file_path)
            self.project.logger.log_error(e)
            self.project.logger.log_error("Could not traverse tree")


    def process_node(self, node):
        if node.grammar_name == "import_declaration":
            self.process_import_declaration(node)
        elif "package_declaration" == node.grammar_name:
            self.process_package(node)
        elif node.grammar_name == "modifiers" and node.parent.grammar_name == "class_declaration":
            self.process_class_modifiers(node)
        elif node.grammar_name == "identifier" and node.parent.grammar_name == "class_declaration":
            self.process_class_name(node)
        elif node.grammar_name == "class_declaration":
            self.process_class_declaration(node)
        elif node.grammar_name == "field_declaration" and node.parent.parent.grammar_name == "class_declaration":
            self.process_class_property(node)
        elif node.grammar_name == "modifiers" and node.parent.grammar_name == "method_declaration":
            self.process_method_modifiers(node)
        elif node.grammar_name == "identifier" and node.parent.grammar_name == "method_declaration":
            self.process_method_name(node)
        elif "type" in node.grammar_name and node.parent.grammar_name == "method_declaration":
            self.process_method_modifiers(node)
        elif node.grammar_name == "method_declaration" or node.grammar_name == "constructor_declaration":
            self.process_method_declaration(node)
        else:
            pass

    def process_import_declaration(self, node):
        file_import = node.text.decode(self.encoding)
        self.data.imports.append(file_import)

    def process_package(self, node):
        namespace = node.text.decode(self.encoding)
        self.data.namespace = namespace

    def process_class_modifiers(self, node):
        class_modifiers = node.text.decode(self.encoding).split("\n")
        for modifier in class_modifiers:
            self.data.modifiers.append(modifier)

    def process_class_name(self, node):
        class_name = node.text.decode(self.encoding)
        self.data.name = class_name

    def process_class_declaration(self, node):
        start_pos = node.start_point
        end_pos = node.end_point
        self.data.start_lin_no = start_pos[0]
        self.data.start_pos = start_pos[1]
        self.data.end_lin_no = end_pos[0]
        self.data.end_pos = end_pos[1]

    def process_class_property(self, node):
        class_property = node.text.decode(self.encoding)
        self.data.properties.append(class_property)

    def process_method_modifiers(self, node):
        method_modifiers = node.text.decode(self.encoding).split("\n")
        for modifier in method_modifiers:
            self.current_method_info.modifiers.append(modifier.strip())

    def process_method_name(self, node):
        method_name = node.text.decode(self.encoding)
        self.current_method_info.name = method_name

    def process_method_declaration(self, node):
        body = node.text.decode(self.encoding)
        start_lin_no = node.start_point[0]
        start_pos = node.start_point[1]
        end_lin_no = node.end_point[0]
        end_pos = node.end_point[1]
        if self.current_method_node is None:
            self.current_method_node = Node
            self.current_method_info = MethodModel()
            self.current_method_info.body = body
            self.current_method_info.start_lin_no = start_lin_no
            self.current_method_info.start_pos = start_pos
            self.current_method_info.end_lin_no = end_lin_no
            self.current_method_info.end_pos = end_pos
        else:
            if self.current_method_info is not None:
                self.data.methods.append(self.current_method_info)

            self.current_method_node = Node
            self.current_method_info = MethodModel()
            self.current_method_info.body = body
            self.current_method_info.start_lin_no = start_lin_no
            self.current_method_info.start_pos = start_pos
            self.current_method_info.end_lin_no = end_lin_no
            self.current_method_info.end_pos = end_pos

