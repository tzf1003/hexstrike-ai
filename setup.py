#!/usr/bin/env python3
"""
HexStrike AI - 安装配置脚本
Setup Configuration Script

用于安装和配置HexStrike AI渗透测试框架
"""

from setuptools import setup, find_packages
import os
import sys

# 检查Python版本
if sys.version_info < (3, 8):
    print("错误: HexStrike AI需要Python 3.8或更高版本")
    print(f"当前版本: {sys.version}")
    sys.exit(1)

# 读取版本信息
def get_version():
    """从__init__.py文件中获取版本号"""
    version_file = os.path.join('hexstrike_ai', '__init__.py')
    if os.path.exists(version_file):
        with open(version_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('__version__'):
                    return line.split('=')[1].strip().strip('"').strip("'")
    return "6.0.0"

# 读取README文件
def get_long_description():
    """获取长描述文本"""
    readme_files = ['README_CN.md', 'README.md']
    for readme_file in readme_files:
        if os.path.exists(readme_file):
            with open(readme_file, 'r', encoding='utf-8') as f:
                return f.read()
    return "HexStrike AI - 高级AI驱动渗透测试框架"

# 读取依赖需求
def get_requirements():
    """获取依赖需求列表"""
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    requirements = []
    for line in lines:
        line = line.strip()
        # 跳过注释和空行
        if line and not line.startswith('#'):
            # 提取包名（去掉版本约束和注释）
            if '#' in line:
                line = line.split('#')[0].strip()
            if line:
                requirements.append(line)
    
    return requirements

# 安装配置
setup(
    # 基本信息
    name="hexstrike-ai",
    version=get_version(),
    description="高级AI驱动渗透测试框架",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    
    # 作者信息
    author="HexStrike AI Team",
    author_email="team@hexstrike.ai",
    url="https://github.com/0x4m4/hexstrike-ai",
    
    # 许可证
    license="MIT",
    
    # 包信息
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'hexstrike_ai': [
            'config/*.py',
            'assets/*',
            '*.json',
            '*.md'
        ],
    },
    
    # 依赖需求
    install_requires=get_requirements(),
    
    # 可选依赖
    extras_require={
        'dev': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.5.0',
        ],
        'docs': [
            'sphinx>=7.1.0',
            'sphinx-rtd-theme>=1.3.0',
            'mkdocs>=1.5.0',
        ],
        'all': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.5.0',
            'sphinx>=7.1.0',
            'sphinx-rtd-theme>=1.3.0',
        ]
    },
    
    # 入口点
    entry_points={
        'console_scripts': [
            'hexstrike=hexstrike_server_new:main',
            'hexstrike-server=hexstrike_server_new:main',
            'hexstrike-mcp=hexstrike_mcp:main',
        ],
    },
    
    # Python版本要求
    python_requires='>=3.8',
    
    # 分类信息
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Security',
        'Topic :: System :: Penetration Testing',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Software Development :: Testing',
        'Environment :: Console',
        'Environment :: Web Environment',
    ],
    
    # 关键词
    keywords=[
        'penetration-testing', 'security', 'ai', 'automation',
        'vulnerability-assessment', 'red-team', 'bug-bounty',
        'ctf', 'security-tools', 'flask', 'mcp'
    ],
    
    # 项目URLs
    project_urls={
        'Bug Reports': 'https://github.com/0x4m4/hexstrike-ai/issues',
        'Source': 'https://github.com/0x4m4/hexstrike-ai',
        'Documentation': 'https://docs.hexstrike.ai',
        'Changelog': 'https://github.com/0x4m4/hexstrike-ai/blob/main/CHANGELOG.md',
    },
    
    # 平台信息
    platforms=['any'],
    
    # zip安全
    zip_safe=False,
)