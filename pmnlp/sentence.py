import re


class SentenceTplTrie:
    """
    用户词语模板trie树，用来获取对应词槽里面的数据，每个词槽均需要初始化一次。
    """

    def __init__(self, word_dict=None):
        """
        由于python dict采用hash存储，因此用dict实现trie树，缺点，就是内存占用稍大。
        """
        self.root = dict()
        self.word_dict = word_dict

    def build(self, sentence_tpl_dict=None, common_key=None):
        if sentence_tpl_dict is None:
            sentence_tpl_dict = {}
        if not (sentence_tpl_dict and isinstance(sentence_tpl_dict, dict)):
            raise Exception('sentence_tpl_dict must be dict')
        for intent, tpl in sentence_tpl_dict.items():
            self.insert(tpl, common_key=common_key, build=True, intent=intent)

    def insert(self, string, common_key=None, intent=None, build=None):
        """
        用于建立和插入trie树。
        @params：string： 用于插入的字符串。
        @common_key: string: 可以用于通用匹配，这个key可以自定义，但是全局必须保持一致。
        @build: 布尔值：用于判断是否处于构建trie树中。
        """
        # 获取中括号中对应的词槽
        word_tpl = re.findall('(?<=\[)[a-zA-Z0-9:-]+(?=\])', string)
        # 将query中的中括号去除，用于保证index没有问题。
        string = re.sub('(\[)|(\])', '', string)
        # 通过查询trie树，获取对应的节点的index和对应的node
        index, node, _ = self.findLastNode(
            string, common_key=common_key, build=build)
        # 用于获取正确的字符串
        string = string[index:]
        # 用于记录获取到的词槽的位置。
        index_word_tpl = {}
        for tpl in word_tpl:
            print('search tpl', index, tpl, string)
            tpl_index = re.search(tpl, string).span()
            for index in tpl_index:
                index_word_tpl[index] = tpl
        # 进行遍历
        tmp_index = 0
        while tmp_index < len(string):
            new_node = dict()
            char = index_word_tpl.get(tmp_index)
            if char:
                tmp_index += len(char)
            else:
                char = string[tmp_index]
                tmp_index += 1
            if tmp_index < len(string):
                node[char] = new_node
                node = new_node
            else:
                node[char] = intent

    def sep(self, string, common_key=None):
        # 进行查询分割，返回值为，查询到的最后的节点，后面的字符串，以及匹配到的结果
        # 最后的匹配结果最为重要，采用元祖的形式返回。
        index, node, result = self.findLastNode(string, common_key=common_key)
        return string[:index], node, result

    def findLastNode(self, string, common_key=None, build=False):
        '''
        @param string: string to be searched
        @return: (index, node).
            index: int. first char(string[index]) of string not found in Trie tree.
            Otherwise, the length of string
            node: dict. node doesn't have string[index].
        '''
        if common_key is None:
            common_key = ''
        node = self.root
        index = 0
        result = []
        while index < len(string):
            char = string[index]
            tmp_string = string[index:]
            # 用于判断node key是什么
            tmp_node_key = list(node.keys())
            if tmp_node_key:
                tmp_node_key = tmp_node_key[0]
            else:
                tmp_node_key = ''
            if common_key and common_key in tmp_node_key:
                # 如果存在common_key， 那么进行common key的获取。
                node = node[tmp_node_key]
                print('tmp_node_key', tmp_node_key, common_key)
                begin, end = tmp_node_key.split(':')[-1].split('-')
                # 进行字符串的通配符匹配，直到获取到对应的内容，或者没有货渠道任何内容。
                for i in range(int(begin), int(end) + 1):
                    common_tmp_string = tmp_string[i:]
                    ttk, ttv = self.map(common_tmp_string,
                                        common_key=common_key)
                    if ttk and ttv:
                        # 如果通配符后面的字符串，获取到对应的内容，则中断通配符匹配，进行后续匹配。
                        break
                    else:
                        index += 1
                        continue
            else:
                ttk, ttv = self.map(
                    tmp_string, common_key=common_key, build=build)
                print('ttk,ttv', ttk, ttv, tmp_string)

            if ttk and ttv:
                if ttk not in node:
                    # 如果正则表达式匹配到了内容，但是匹配到的不是当前节点，则index+1继续匹配。
                    index += 1
                    continue
                node = node[ttk]
                index += len(ttv)
                result.append((ttk, ttv))
            elif char in node:
                node = node[char]
                print(node)
                index += 1
            else:
                print('breaking', string, node, result, index)
                break
            if isinstance(node, str):
                break
        return (index, node, result)

    def map(self, string, common_key=None, build=None):
        # 查找对应的词槽对应的内容。
        print('\nword_dict:', string, )
        for k, v in self.word_dict.items():
            print('\nword_dict:', v, string, k)
            word, _ = v.sep(string, build=build)
            if word:
                print('\nword_dict:', string, k, word)
                return k, word
            else:
                continue
        return None, None
