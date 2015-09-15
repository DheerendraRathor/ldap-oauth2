default_fields = ['id', 'username', 'first_name', 'last_name', 'email']
user_fields = ['program', 'secondary_emails', 'contacts', 'insti_address']

scope_to_field_map = {
    'basic': ['id', 'username', 'first_name', 'last_name', 'email'],
    'phone': ['contacts'],
    'insti_address': ['insti_address'],
    'program': ['program'],
    'secondary_emails': ['secondary_emails'],
}