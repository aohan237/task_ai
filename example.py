from pmnlp.word import build_sentence_word_dict
from pmnlp.sentence import SentenceTplTrie


# 初始化，用于记录用户配置的词槽，以及语句的模版匹配。

user_word_dict = {'num': ['一杯', '两杯', '三杯'], 'coffee': [
    '拿铁', '拿铁咖啡'], 'common': [], 'phone': ['re\d+']}
sentent_intent_tpl = {
    'coffee': '[common:0-4][num][common:0-10][coffee]'
}

# # 建立模型
# sentence_word_dict = build_sentence_word_dict(word_dict=user_word_dict)
# 支持模糊拼音，南方的朋友有福了
sentence_word_dict = build_sentence_word_dict(
    word_dict=user_word_dict, fuzzy=True)

test_tree = SentenceTplTrie(word_dict=sentence_word_dict)
test_tree.build(sentence_tpl_dict=sentent_intent_tpl, common_key='common')


# 理解用户输入
_, intent, result = test_tree.sep('我要山杯热啊啊啊啊啊啊那铁咖啡', common_key='common')
if isinstance(intent, str):
    print(intent, result)
else:
    print(intent, result)
