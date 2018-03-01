import re


class WordTrie:
    def __init__(self):
        # 初始化词表。
        self.root = dict()

    def __repr__(self):
        # console的字符串显示。
        return str(self.root)

    def insert(self, string):
        # 添加词语到此词表中。
        index, node = self.findLastNode(string)
        if 're' in string:
            char = string
            new_node = dict()
            node[char] = new_node
            new_node = new_node
        else:
            for char in string[index:]:
                new_node = dict()
                node[char] = new_node
                node = new_node

    def sep(self, string, build=None):
        # 用于分割字符串，然后进行字符串的操作。
        index, node = self.findLastNode(string)
        tmp_node_key = list(node.keys())
        if tmp_node_key:
            tmp_node_key = tmp_node_key[0]
        else:
            tmp_node_key = ''
        if not build and 're' in tmp_node_key:
            tmp_node_key = tmp_node_key.replace('re', '')
            result = re.findall(tmp_node_key, string[index:])
            if result:
                result = result[0]
            else:
                result = string[:index]
            return result, string[index:]
        else:
            return string[:index], string[index:]

    def findLastNode(self, string):
        '''
        寻找最后的节点，然后进行对应的操作。
        @param string: string to be searched
        @return: (index, node).
            index: int. first char(string[index]) of string not found in Trie tree. Otherwise, the length of string
            node: dict. node doesn't have string[index].
        '''
        node = self.root
        index = 0
        if 're' in string:
            char = string
            if char in node:
                node = node[char]
        else:
            while index < len(string):
                char = string[index]
                if char in node:
                    node = node[char]
                else:
                    break
                index += 1
        return (index, node)


def build_sentence_word_dict(word_dict=None):
    if word_dict is None:
        word_dict = {}
    if not (word_dict and isinstance(word_dict, dict)):
        raise Exception('word_dict must be dict')
    sentence_word_dict = {}
    for k, v in word_dict.items():
        tmp_trie = WordTrie()
        for i in v:
            tmp_trie.insert(i)
        sentence_word_dict[k] = tmp_trie
    return sentence_word_dict
