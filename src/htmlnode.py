from textnode import TextNode, TextType

class HTMLNode:
	def __init__(self, tag=None, value=None, children=None, props=None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self):
		raise NotImplementedError

	def props_to_html(self):
		html_string = ""
		if self.props == None:
			return ""
		for key, value in self.props.items():
			html_string += f' {key}="{value}"'
		return html_string

	def __repr__(self):
		return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"


class LeafNode(HTMLNode):
	def __init__(self, tag, value, props=None):
		super().__init__(tag, value, None, props)

	def to_html(self):
		if self.value is None:
                        raise ValueError("LeafNode must have a value")

		if self.tag is None:
			return self.value

		html_rend = f"<{self.tag}"

		if self.props:
			for prop, value in self.props.items():
				html_rend += f' {prop}="{value}"'

		html_rend += f">{self.value}</{self.tag}>"

		return html_rend


class ParentNode(HTMLNode):
	def __init__(self, tag, children, props=None):
		super().__init__(tag, None, children, props)

	def to_html(self):
		if self.tag is None:
			raise ValueError("ParentNode must have a tag")

		if self.children is None:
			raise ValueError("ParentNode must have children")

		html_string = f"<{self.tag}>"

		for child in self.children:
			html_string += child.to_html()

		html_string += f"</{self.tag}>"

		return html_string


def text_node_to_html_node(text_node):
	match text_node.text_type:
		case TextType.TEXT:
			return LeafNode(None, text_node.text)
		case TextType.BOLD:
			return LeafNode("b", text_node.text)
		case TextType.ITALIC:
			return LeafNode("i", text_node.text)
		case TextType.CODE:
			return LeafNode("code", text_node.text)
		case TextType.LINK:
			return LeafNode("a", text_node.text, {"href": text_node.url})
		case TextType.IMAGE:
			return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
		case _:
			raise ValueError(f"Invalid TextType: {text_node.text_type}")
