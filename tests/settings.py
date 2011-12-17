DATABASES = {
    'default': {
        'ENGINE': 'sqlite3',
        'NAME': ':memory:'
    }
}

INSTALLED_APPS = [
    'kronos',
    'tests.app'
]

ROOT_URLCONF = 'tests.app.urls'
