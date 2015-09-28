default_fields = ['id', 'username', 'first_name', 'last_name', 'email', ]
user_fields = ['program', 'secondary_emails', 'contacts', 'insti_address', 'mobile', 'roll_number', ]

scope_to_field_map = {
    'basic': ['id', 'username', 'first_name', 'last_name', 'email', ],
    'phone': ['contacts', 'mobile', ],
    'insti_address': ['insti_address', ],
    'program': ['program', 'roll_number', ],
    'secondary_emails': ['secondary_emails', ],
}