from setuptools import setup

APP = ['app.py']
DATA_FILES = [
    ('', ['passwd-CN-Top10000.txt'])  # 使用相對路徑
]

OPTIONS = {
    'argv_emulation': False,  # 改為 False
    'packages': [
        'selenium',
        'trio',
        'attrs',
        'certifi',
        'idna',
        'outcome',
        'sniffio',
        'sortedcontainers',
        'trio_websocket',
        'typing_extensions',
        'urllib3',
        'wsproto',
        'websocket',
        'socks'
    ],
    'includes': [
        'h11',
        'pkg_resources',
        'packaging',
        'setuptools'
    ],
    'excludes': [
        'tkinter',
        'matplotlib',
        'PIL'
    ],
    'iconfile': 'logo.icns',  # 使用相對路徑
    'plist': {
        'CFBundleName': 'RainbowCrack',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'CFBundleIdentifier': 'com.lwopan.rainbowcrack',
        'LSMinimumSystemVersion': '10.10',
        'NSHighResolutionCapable': True,
    },
    'resources': ['passwd-CN-Top10000.txt'],  # 添加資源文件
    'site_packages': True,  # 確保包含所有site-packages
    'strip': True,  # 減少檔案大小
}

setup(
    name='RainbowCrack',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=[
        'selenium>=4.25.0',
        'trio>=0.26.2',
        'attrs>=24.2.0',
        'certifi>=2024.8.30',
        'h11>=0.14.0',
        'idna>=3.10',
        'outcome>=1.3.0.post0',
        'PySocks>=1.7.1',
        'sniffio>=1.3.1',
        'sortedcontainers>=2.4.0',
        'trio-websocket>=0.11.1',
        'typing_extensions>=4.12.2',
        'urllib3>=2.2.3',
        'websocket-client>=1.8.0',
        'wsproto>=1.2.0'
    ]
)