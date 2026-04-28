from domain.enum.role import Role

class Constants:

    CODE_CANNOT_BE_EMPTY = "Code cannot be empty"
    PLATE_CANNOT_BE_EMPTY = "Plate cannot be empty"
    PLATE_MUST_BE_7_CHARACTERS = "Plate must be 7 characters (got {length})"
    INVALID_PLATE_FORMAT = "Invalid plate format: {plate}"
    KM_CANNOT_BE_NEGATIVE = "Km cannot be negative"
    FUEL_LEVEL_CANNOT_BE_NEGATIVE = "Fuel level cannot be negative"
    FUEL_CARD_CANNOT_BE_EMPTY = "Fuel card cannot be empty"

    CODE_CANNOT_BE_EMPTY = "Code cannot be empty"
    DESCRIPTION_CANNOT_BE_EMPTY = "Description cannot be empty"

    CART_NUMBER_CANNOT_BE_EMPTY = "Cart number cannot be empty"
    LITER_PRICE_CANNOT_BE_NEGATIVE = "Liter price cannot be negative"
    LITERS_CANNOT_BE_NEGATIVE = "Liters cannot be negative"
    RECEIPT_PHOTO_CANNOT_BE_EMPTY = "Receipt photo cannot be empty"

    START_POSITION_CANNOT_BE_EMPTY = "Start position cannot be empty"
    END_POSITION_CANNOT_BE_EMPTY = "End position cannot be empty"
    START_DATE_CANNOT_BE_IN_THE_FUTURE = "Start date cannot be in the future"
    END_DATE_CANNOT_BE_IN_THE_FUTURE = "End date cannot be in the future"
    START_KM_CANNOT_BE_NEGATIVE = "Start km cannot be negative"

    KM_TOTAL_CANNOT_BE_NEGATIVE = "Total km cannot be negative"
    KM_SERVICING_CANNOT_BE_NEGATIVE = "Servicing km cannot be negative"
    KM_WHEELS_CANNOT_BE_NEGATIVE = "Wheels km cannot be negative"

    NAME_CANNOT_BE_EMPTY = "Name cannot be empty"
    EMAIL_CANNOT_BE_EMPTY = "Email cannot be empty"
    PASSWORD_CANNOT_BE_EMPTY = "Password cannot be empty"
    HASHED_PASSWORD_CANNOT_BE_EMPTY = "Hashed password cannot be empty"
    INVALID_ROLE = "Invalid role"

    EMAIL_ALREADY_EXISTS = "Email already exists"
    EMAIL_ALREADY_USE = "Email already in use"
    USER_NOT_FOUND = "User not found"
    INVALID_CREDENTIALS = "Invalid credentials"

    CAR_NOT_FOUND = "Car not found"
    COMMIT_NOT_FOUND = "Commit not found"
    REFUELING_NOT_FOUND = "Refueling not found"
    TRIP_NOT_FOUND = "Trip not found"
    USER_NOT_OWNER = "User is not the owner of the resource"
    REFUELING_NOT_FOUND = "Refueling not found"

    CAR_ALREADY_EXISTS = "Car with the same plate already exists"

    JWT_SECRET = "JWT_SECRET"
    DEV_SECRET = "dev-secret"

    INVALID_TOKEN = "Invalid token"

    USER_ROLE_REQUIRED = "User role required"
    ADMIN_ROLE_REQUIRED = "Admin role required"

    ROLE="role"

    SUB="sub"

    SUPPORTED_BASE_API_ROLES = [Role.ADMIN.value, Role.USER.value]

    API_V1_PREFIX = "/api/v1/lambdacar"

    BEARER = "bearer"

    ADMIN = "admin"
    USER = "user"

    GASOLINE = "gasoline"
    DIESEL = "diesel"
    ADBLUE = "adblue"
    GPL = "GPL"
    METHANE = "methane"
    ELECTRIC = "electric"