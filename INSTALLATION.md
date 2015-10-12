Installation Guidelines
=======================

It is easy to make local copy of this project. All you need is Python 2.7!  
If you've never used virtualenv before, you'll advise you to read about 
[virtualenv](https://virtualenv.pypa.io/en/latest/) and 
[virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/)

*virtualenv is not required for this project, but you should use it as a good python development practice*

Steps:
------
1. Install all requirements by running `pip install -r requirements.txt` in project root
    - To install some python libraries like `python-ldap` or `psycopg2` you might need to install some OS based 
    packages. Please refer to their individual installation guideline on their homepages
2. Copy configurable settings file `sso/settings_user.py.sample` to `sso/settings_user.py`
3. Edit `sso/settings_user.py` and add configurations and credentials
4. If you are planning to run in production, you should add database settings in `sso/settings_user.py`
5. Add `SECRET_KEY` in `sso/settings_user.py`   
6. Run migrations by `python manage.py migrate`
7. Create superuser by running `python manage.py createsuperuser`
8. Run `python manage.py runserver`. Open browser at `http://localhost:8000/`
9. Congrats! Installation is complete!