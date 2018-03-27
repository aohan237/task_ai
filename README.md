# 简单的 任务式 自然语言理解 工具

## 最近更新

增加拼音模糊识别，并返回正确的你需要的内容

## 说明

支持中文语句的模版匹配。可以理解为，简单版本的百度unit或者科大讯飞的AIUI

对于，简单语句的自然语言理解也是很方便的。欢迎大家试用。

对于不喜欢调用API，喜欢在自己代码中嵌入的人是蛮好用的。

## 用例

    ```
    from pmnlp.word import build_sentence_word_dict
    from pmnlp.sentence import SentenceTplTrie

    # 初始化，用于记录用户配置的词槽，以及语句的模版匹配。
    user_word_dict = {'num': ['一杯', '两杯', '三杯'], 'coffee': [
        '拿铁', '拿铁咖啡'], 'common': [], 'phone': ['re\d+']}
    sentent_intent_tpl = {
        'coffee': '[common:0-4][num][common:0-10][coffee]'
    }

    # 建立模型

    sentence_word_dict = build_sentence_word_dict(word_dict=user_word_dict)

    # 支持模糊拼音，南方的朋友有福了  fuzzy表示是否支持模糊拼音
    sentence_word_dict = build_sentence_word_dict(
        word_dict=user_word_dict, fuzzy=True)

    test_tree = SentenceTplTrie(word_dict=sentence_word_dict)
    test_tree.build(sentence_tpl_dict=sentent_intent_tpl, common_key='common')


    # 理解用户输入
    _, intent, result = test_tree.sep('我要山杯热啊啊啊啊啊啊拿铁咖啡',common_key='common')
    if isinstance(intent, str):
        print(intent, result)
    else:
        print(intent, result)
    ```