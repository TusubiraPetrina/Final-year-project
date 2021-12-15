from django.contrib.auth.models import User

def createSuperUser(username, password, email="", firstName="", lastName=""):
    invalidInputs = ["", None]

    if username.strip() in invalidInputs or password.strip() in invalidInputs:
        return None

    user = User(
        username = username,
        email = email,
        first_name = firstName,
        last_name = lastName
    )

    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    
    user.save()

    return user