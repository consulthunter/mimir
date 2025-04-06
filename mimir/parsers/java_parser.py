import tree_sitter_java as ts_java
from tree_sitter import Node
from typing import Generator

from mimir.models.class_model import ClassModel
from mimir.models.code_model import CodeModel
from mimir.models.method_model import MethodModel
from mimir.parsers.base_parser import BaseParser

class JavaParser(BaseParser):

    def __init__(self, project, file_path):
        self.file_path = str(file_path)
        self.project = project
        super().__init__(ts_java.language())
        self.tree = self.parse_file(file_path)
        self.data = CodeModel("java")

        self.classes = []

        try:
            for node in self.traverse_children(self.tree.root_node):
                self.process_child(node)
        except Exception as e:
            self.project.logger.log_error(f"Error parsing {self.file_path}: {e}")

        for c in self.classes:
            self.data.code_classes.append(c)

        try:
            self.project.data[self.file_path] = self.data
        except Exception as e:
            self.project.logger.log_error(f"Error saving parsed code data to model {e}")


    def traverse_children(self, node)-> Generator[Node, None, None]:
        try:
            cursor = node.walk()

            # Skip the root node and go directly to the first child
            if cursor.goto_first_child():
                # Yield only immediate children of the root
                while cursor.node is not None:
                    yield cursor.node
                    # Move to the next sibling
                    if not cursor.goto_next_sibling():
                        break
            else:
                # In case there are no children
                yield from ()  # Return an empty generator if there are no children

        except Exception as e:
            self.project.logger.log_info(self.file_path)
            self.project.logger.log_error(e)
            self.project.logger.log_error("Could not traverse tree")

    def traverse_whole_tree(self) -> Generator[Node, None, None]:
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


    def process_child(self, node):
        if node.grammar_name == "import_declaration":
            self.process_import_declaration(node)
        elif node.grammar_name == "package_declaration":
            self.process_package(node)
        elif node.grammar_name == "class_declaration":
            self.process_class_node(node)
        else:
            pass

    def process_class_child(self, node, class_model: ClassModel):
        if node.grammar_name == "class_declaration":
            self.process_class_node(node)
        elif node.grammar_name == "modifiers" and node.parent.grammar_name == "class_declaration":
            self.process_class_modifiers(node, class_model)
        elif node.grammar_name == "identifier" and node.parent.grammar_name == "class_declaration":
            self.process_class_name(node, class_model)
        elif node.grammar_name == "field_declaration" and node.parent.parent.grammar_name == "class_declaration":
            self.process_class_property(node, class_model)
        elif node.grammar_name == "method_declaration" or node.grammar_name == "constructor_declaration":
            self.process_method_node(node, class_model)
        else:
            pass

    def process_method_child(self, node, method_model: MethodModel):
        if node.grammar_name == "modifiers" and node.parent.grammar_name == "method_declaration":
            self.process_method_modifiers(node, method_model)
        elif node.grammar_name == "identifier" and node.parent.grammar_name == "method_declaration":
            self.process_method_name(node, method_model)
        elif "type" in node.grammar_name and node.parent.grammar_name == "method_declaration":
            self.process_method_modifiers(node, method_model)
        else:
            pass

    def process_class_node(self, node):
        java_class = ClassModel()
        start_pos = node.start_point
        end_pos = node.end_point
        java_class.start_lin_no = start_pos[0]
        java_class.start_pos = start_pos[1]
        java_class.end_lin_no = end_pos[0]
        java_class.end_pos = end_pos[1]

        self.classes.append(java_class)

        for node in self.traverse_children(node):
            self.process_class_child(node, java_class)
            if node.grammar_name == "class_body":
                body_node = node
                for node in self.traverse_children(node):
                    self.process_class_child(node, java_class)

    def process_method_node(self, node, class_model: ClassModel):
        java_method = MethodModel()
        class_model.methods.append(java_method)

        java_method.body = node.text.decode(self.encoding)
        java_method.start_lin_no = node.start_point[0]
        java_method.start_pos = node.start_point[1]
        java_method.end_lin_no = node.end_point[0]
        java_method.end_pos = node.end_point[1]

        for node in self.traverse_children(node):
            self.process_method_child(node, java_method)


    def process_import_declaration(self, node):
        file_import = node.text.decode(self.encoding)
        self.data.imports.append(file_import)

    def process_package(self, node):
        namespace = node.text.decode(self.encoding)
        self.data.namespace = namespace

    def process_class_modifiers(self, node, class_model: ClassModel):
        class_modifiers = node.text.decode(self.encoding).split("\n")
        for modifier in class_modifiers:
            class_model.modifiers.append(modifier)

    def process_class_name(self, node, class_model: ClassModel):
        class_name = node.text.decode(self.encoding)
        class_model.name = class_name

    def process_class_property(self, node, class_model: ClassModel):
        class_property = node.text.decode(self.encoding)
        class_model.properties.append(class_property)

    def process_method_modifiers(self, node, method_model: MethodModel):
        method_modifiers = node.text.decode(self.encoding).split("\n")
        for modifier in method_modifiers:
            method_model.modifiers.append(modifier.strip())

    def process_method_name(self, node, method_model: MethodModel):
        method_name = node.text.decode(self.encoding)
        method_model.name = method_name