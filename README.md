OAUTH 2.0 Provider for LDAP
===========================
This application usage the standard OAuth2.0 flow described in [RFC 6749](https://tools.ietf.org/html/rfc6749) 

URLs:
-----
**All URLs are from base of application URL. (i.e. assuming application is installed at '/')**  
* Application Registration `/oauth/applications/`
* Authorization `/oauth/authorize/`
* Get Access Token `/oauth/token/`
* Revoke Token `/oauth/revoke_token/`

Scopes:
-------
* **basic**: *Basic profile information including first name, last name and email*
* **phone**: *Your contact number including additional numbers*
* **insti_address**: *Your address inside institute*
* **program**: *Your roll number, department, course, joining year and graduation year*
* **secondary_emails**: *Your alternate emails*

User Resources:
---------------
* **/user/api/user/**: Get basic information corresponding to **basic** scope
* **/user/api/user/?fields=field1,field2**: Get additional information corresponding to field1 and field2. See available fields below

Fields:
-------
**Field Name**: *Required Scopes*
* **contacts**: *phone*
* **insti_address**: *insti_address*
* **program**: *program*
* **secondary_emails**: *secondary_emails*

TODO:
-----
* Atomize permissions
* Add endpoint to send email on behalf of app

