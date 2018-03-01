import re
import os.path
import sys
from setuptools import setup, find_packages


install_requires = ['re']

PY_VER = sys.version_info

if PY_VER >= (3, 4):
    pass
elif PY_VER >= (3, 3):
    pass
else:
    raise RuntimeError("pmnlp doesn't support Python version prior 3.3")


def read(*parts):
    with open(os.path.join(*parts), 'rt') as f:
        return f.read().strip()


def read_version():
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = os.path.join(os.path.dirname(__file__),
                           'pmnlp', '__init__.py')
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        else:
            raise RuntimeError('Cannot find version in pmnlp/__init__.py')


classifiers = [
    'License :: OSI Approved :: MIT License',
    'Development Status :: 4 - Beta',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Operating System :: POSIX',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries',
]

long_description = "简单的 任务式 自然语言理解 工具\n===============================\n\n说明\n----\n\n支持中文语句的模版匹配。可以理解为，简单版本的百度unit或者科大讯飞的AIUI\n\n对于，简单语句的自然语言理解也是很方便的。欢迎大家试用。\n\n对于不喜欢调用API，喜欢在自己代码中嵌入的人是蛮好用的。\n\n用例\n----\n\n::\n\n    ```\n    from pmnlp.word import build_sentence_word_dict\n    from pmnlp.sentence import SentenceTplTrie\n\n    # 初始化，用于记录用户配置的词槽，以及语句的模版匹配。\n    user_word_dict = {'num': ['一杯', '两杯'], 'coffee': [\n        '拿铁', '拿铁咖啡'], 'common': [], 'phone': ['re\\d+']}\n    sentent_intent_tpl = {\n        'coffee': '[common:0-4][num][common:0-10][coffee]'\n    }\n\n    # 建立模型\n    sentence_word_dict = build_sentence_word_dict(word_dict=user_word_dict)\n    test_tree = SentenceTplTrie(word_dict=sentence_word_dict)\n    test_tree.build(sentence_tpl_dict=sentent_intent_tpl, common_key='common')\n\n\n    # 理解用户输入\n    _, intent, result = test_tree.sep('我要一杯热啊啊啊啊啊啊拿铁咖啡',common_key='common')\n    if isinstance(intent, str):\n        print(intent, result)\n    else:\n        print(intent, result)\n    ```\n"

setup(name='pmnlp',
      version=read_version(),
      description=("pattern match for nlp"),
      long_description=long_description,
      classifiers=classifiers,
      platforms=["POSIX"],
      author="aohan237",
      author_email="aohan237@gmail.com",
      url="https://github.com/aohan237/pmnlp",
      license="MIT",
      packages=find_packages(exclude=["tests"]),
      install_requires=install_requires,
      include_package_data=True,
      )
