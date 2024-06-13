MALE = 'male'
FEMALE = 'female'
OTHER = 'other'

SINGLE = 'single'
MARRIED = 'married'
DIVORCED = 'divorced'
WIDOWED = 'widowed'

ADD = 'add'
VIEW = 'view'
EDIT = 'edit'
DELETE = 'delete'

GENDER_CHOICES = [
    (MALE, 'Male'),
    (FEMALE, 'Female'),
    (OTHER, 'Other'),
]

MARIATAL_STATUS_CHOICES = [
    (SINGLE, 'Single'),
    (MARRIED, 'Married'),
    (DIVORCED, 'Divorced'),
    (WIDOWED, 'Widowed'),
]

PERMISSION_CHOICES = [
    (ADD, 'add'),
    (VIEW, 'View'),
    (EDIT, 'Edit'),
    (DELETE, 'delete'),
]