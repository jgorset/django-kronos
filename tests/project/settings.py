DATABASES = {
    'default': {
        'ENGINE': 'sqlite3',
        'NAME': ':memory:'
    }
}

INSTALLED_APPS = [
    'kronos',
    'tests.project.app'
]

ROOT_URLCONF = 'urls'
