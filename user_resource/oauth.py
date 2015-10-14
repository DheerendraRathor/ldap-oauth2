default_fields = ['id', ]
user_fields = [
    'username',
    'first_name',
    'last_name',
    'profile_picture',
    'email',
    'program',
    'secondary_emails',
    'contacts',
    'insti_address',
    'mobile',
    'roll_number',
]

scope_to_field_map = {
    'basic': ['id', ],
    'profile': ['first_name', 'last_name'],
    'picture': ['profile_picture'],
    'ldap': ['username', 'email'],
    'phone': ['contacts', 'mobile', ],
    'insti_address': ['insti_address', ],
    'program': ['program', 'roll_number', ],
    'secondary_emails': ['secondary_emails', ],
    'send_mail': [],
}
