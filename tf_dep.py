#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import os

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def read_text_from_repo(repo, subpath):
    """Read text from file of github or local filesystem

    Arguments:
        repo (str): repo path for local or github, such as:
            - local file: `C:\\projects\\tensorflow`
            - github: 
                - `github:tensorflow/tensorflow/master`
                - `github:tensorflow/tensorflow/v2.1.0`
        subpath (str): file path in tensorflow repo which is forbidden to start with slash
    """
    if repo.startswith('github:'):
        repo_addr = repo[7:].strip('/')
        num_args = len(repo_addr.split('/'))
        if num_args == 2:
            repo_addr += '/master'
        elif num_args == 3:
            pass
        else:
            raise ValueError(
                'Unsupported github repo type, it should be like `github:tensorflow/tensorflow[/master]`')
        repo_file_url = 'https://raw.githubusercontent.com/{}/{}'.format(
            repo_addr, subpath)
        content = requests.get(repo_file_url).content.decode('utf-8')
    else:
        repo_file_path = os.path.normpath(os.path.join(repo, subpath))
        with open(repo_file_path, 'rt', encoding='utf-8') as fp:
            content = fp.read()

    return content


def _group_first(re_result):
    return None if re_result is None else re_result.groups()[0]


def _strip_and_unquote(s):
    return s.strip(' \t\n\r"\'')


def _parse_configure_py(content):
    info = {}
    _filters = [
        {
            'match': '_DEFAULT_CUDA_VERSION',
            'target': 'cuda',
            'formatter': _strip_and_unquote
        }, {
            'match': '_DEFAULT_CUDNN_VERSION',
            'target': 'cudnn',
            'formatter': _strip_and_unquote
        }, {
            'match': '_DEFAULT_TENSORRT_VERSION',
            'target': 'tensor_rt',
            'formatter': _strip_and_unquote
        }, {
            'match': '_DEFAULT_CUDA_COMPUTE_CAPABILITIES',
            'target': 'cuda_compute',
            'formatter': _strip_and_unquote
        }, {
            'match': '_TF_CURRENT_BAZEL_VERSION',
            'target': 'bazel',
            'formatter': _strip_and_unquote
        }, {
            'match': '_TF_MIN_BAZEL_VERSION',
            'target': 'bazel_min',
            'formatter': _strip_and_unquote
        }, {
            'match': '_TF_MAX_BAZEL_VERSION',
            'target': 'bazel_max',
            'formatter': _strip_and_unquote
        },
    ]

    for _line in content.splitlines():
        _result = re.match(r'^(\S+)\s*=\s*(.*)\s*$', _line)
        if _result:
            k, v = _result.groups()
            for idx, _filter in enumerate(_filters):
                if _filter['match'] == k:
                    if v == 'None':
                        continue
                    info[_filter['target']] = _filter['formatter'](v)
                    del _filters[idx]
                    break
        if not _filters:
            break

    return info


def parse_tf_repo(repo='github:tensorflow/tensorflow/master'):
    tf_dep_info = {}

    # parse info from configure.py
    content = read_text_from_repo(repo, 'configure.py')
    tf_dep_info.update(_parse_configure_py(content))

    if not tf_dep_info.get('bazel'):
        # parse bazel version used in CI
        content = read_text_from_repo(
            repo,
            'tensorflow/tools/ci_build/install/install_bazel.sh')
        res = re.search(
            '^BAZEL_VERSION=["\']?([0-9.]+)["\']?', content, flags=re.MULTILINE)
        tf_dep_info['bazel'] = _group_first(res)

    if not tf_dep_info.get('bazel_min'):
        # parse bazel minimal version in WORKSPACE
        content = read_text_from_repo(repo, 'WORKSPACE')
        res = re.search(
            '^check_bazel_version_at_least\\(["\']([0-9.]+)["\']\\)', content, flags=re.MULTILINE)
        tf_dep_info['bazel_minimal'] = _group_first(res)

    return tf_dep_info


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    # parser.add_argument('--http-proxy', dest='http_proxy')
    parser.add_argument(
        'repo', help='tensorflow repo path, current only supported github and local filesystem')
    args = parser.parse_args()

    result = parse_tf_repo(args.repo)
    print(result)
