DEFAULT_FIELDS = ['id', ]
USER_FIELDS = [
    'username',
    'first_name',
    'last_name',
    'type',
    'is_alumni',
    'sex',
    'profile_picture',
    'email',
    'program',
    'secondary_emails',
    'contacts',
    'insti_address',
    'mobile',
    'roll_number',
]

SCOPE_TO_FIELD_MAP = {
    'basic': ['id', ],
    'profile': ['first_name', 'last_name', 'type', 'is_alumni', ],
    'sex': ['sex', ],
    'picture': ['profile_picture'],
    'ldap': ['username', 'email'],
    'phone': ['contacts', 'mobile', ],
    'insti_address': ['insti_address', ],
    'program': ['program', 'roll_number', ],
    'secondary_emails': ['secondary_emails', ],
    'send_mail': [],
}
