from django.conf import settings
from django.db.models.fields import BLANK_CHOICE_DASH

def get_default_scopes(application):
    if application.is_anonymous:
        return application.required_scopes.split()
    return settings.OAUTH2_DEFAULT_SCOPES


SEXES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]

BLANK_SEXES = BLANK_CHOICE_DASH + SEXES

DISCIPLINES = [
    # Departments
    ['AE', 'Aerospace Engineering'],
    ['BB', 'Biosciences and Bioengineering'],
    ['CHE', 'Chemical Engineering'],
    ['CH', 'Chemistry'],
    ['CLE', 'Civil Engineering'],
    ['CSE', 'Computer Science & Engineering'],
    ['ES', 'Earth Sciences'],
    ['EE', 'Electrical Engineering'],
    ['ESE', 'Energy Science and Engineering'],
    ['HSS', 'Humanities & Social Science'],
    ['IDC', 'Industrial Design Centre'],
    ['MM', 'Mathematics'],
    ['ME', 'Mechanical Engineering'],
    ['MEMS', 'Metallurgical Engineering & Materials Science'],
    ['PH', 'Physics'],
    ['MS', 'Material Science'],
    ['PHE', 'Physical Education'],
    ['PMS', 'Physics, Material Science'],
    ['PC', 'Preparatory Course'],
    ['RE', 'Reliability Engineering'],

    # Centers
    ['ASC', 'Application Software Centre'],
    ['CRNTS', 'Centre for Research in Nanotechnology and Science'],
    ['CASDE', 'Centre for Aerospace Systems Design and Engineering'],
    ['CC', 'Computer Centre'],
    ['CDEEP', 'Centre for Distance Engineering Education Programme'],
    ['CESE', 'Centre for Environmental Science and Engineering'],
    ['CSRE', 'Centre of Studies in Resources Engineering'],
    ['CTARA', 'Centre for Technology Alternatives for Rural Areas'],
    ['CFDVS', 'Centre for Formal Design and Verification of Software'],
    ['CUSE', 'Centre for Urban Science and Engineering'],
    ['DSCE', 'Desai Sethi Centre for Entrepreneurship'],
    ['IITBMRA', 'IITB-Monash Research Academy'],
    ['NCAIR', 'National Centre for Aerospace Innovation and Research'],
    ['NCM', 'National Centre for Mathematics'],
    ['SAIF', 'Sophisticated Analytical Instrument Facility'],
    ['TCTD', 'Tata Center for Technology and Design'],
    ['WRCB', 'Wadhwani Research Centre for Bioengineering'],
    ['BIOTECH', 'Biotechnology'],

    # School
    ['SJMSOM', 'Shailesh J. Mehta School of Management'],
    ['KReSIT', 'Kanwal Rekhi School of Information Technology'],

    # Interdisciplinary Programs
    ['CLS', 'Climate Studies'],
    ['ET', 'Educational Technology'],
    ['IEOR', 'Industrial Engineering and Operations Research'],
    ['SCE', 'Systems and Control Engineering'],

    # IDC
    ['ANIM', 'Animation'],
    ['IDC', 'Industrial Design Centre'],
    ['IxD', 'Interaction Design'],
    ['MVD', 'Mobility and Vehicle Design'],
    ['VISCOM', 'Visual Communication'],

    # Others
    ['IM', 'Industrial Management'],
    ['MMM', 'Materials, Manufacturing and Modelling'],
    ['CORRSCI', 'Corrosion Science and Engineering'],
    ['CEP', 'Continuing Education Programme'],
    ['AGP', 'Applied Geophysics'],
    ['ASI', 'Applied Statistics and Informatics'],
    ['BME', 'Biomedical Engineering'],
]

SORTED_DISCIPLINES = sorted(DISCIPLINES, key=lambda x: x[1])

DEGREES = [
    ['BTECH', 'Bachelor of Technology'],
    ['MTECH', 'Master of Technology'],
    ['DD', 'B.Tech. + M.Tech. Dual Degree'],
    ['MSC', 'Master of Science'],
    ['PHD', 'Doctor of Philosophy'],
    ['BDES', 'Bachelor of Design'],
    ['MDES', 'Master of Design'],
    ['MPHIL', 'Master of Philosophy'],
    ['MMG', 'Master of Management'],
    ['MSEx', 'M.S. (Exit Degree)'],
    ['MtechEx', 'Master of Technology (Exit Degree)'],
    ['MtechPhDDD', 'M.Tech. + Ph.D. Dual Degree'],
    ['PC', 'Preparatory Course'],
    ['VS', 'Visiting Student'],
    ['MPhilEx', 'Master of Philosophy (Exit Degree)'],
    ['MScEx', 'Master of Science (Exit Degree)'],
    ['MScMTechDD', 'M.Sc. + M.Tech. Dual Degree'],
    ['MScPhDDD', 'M.Sc. + Ph.D. Dual Degree'],
    ['MPhilPhDDD', 'M.Phil. + Ph.D. Dual Degree'],
    ['EMBA', 'Executive MBA'],
    ['FYBS', 'Four Year BS'],
    ['IMTECH', 'Integrated M.Tech.'],
    ['MSCBR', 'Master of Science By Research'],
    ['TYMSC', 'Two Year M.Sc.'],
    ['FYIMSC', 'Five Year Integrated M.Sc.'],
    ['DIIT', 'D.I.I.T.'],
    ['DIITEx', 'D.I.T.T. (Exit Degree)'],
]

HOSTELS = [
    ['1', 'Hostel 1'],
    ['2', 'Hostel 2'],
    ['3', 'Hostel 3'],
    ['4', 'Hostel 4'],
    ['5', 'Hostel 5'],
    ['6', 'Hostel 6'],
    ['7', 'Hostel 7'],
    ['8', 'Hostel 8'],
    ['9', 'Hostel 9'],
    ['10', 'Hostel 10'],
    ['10A', 'Hostel 10A'],
    ['11', 'Hostel 11'],
    ['12', 'Hostel 12'],
    ['13', 'Hostel 13'],
    ['14', 'Hostel 14'],
    ['15', 'Hostel 15'],
    ['16', 'Hostel 16'],
    ['tansa', 'Tansa'],
    ['qip', 'QIP'],
]
