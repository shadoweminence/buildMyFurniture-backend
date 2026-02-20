# myproject/utils.py
from rest_framework.views import exception_handler

# this is to simplify and make the error message similar for frontend use


def custom_exception_handler(exc, context):
    # Call DRF's default handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Flatten the error detail into a single "error" field
        if isinstance(response.data, dict):
            # Take first error message available
            error_messages = []
            for key, value in response.data.items():
                if isinstance(value, list):
                    error_messages.append(str(value[0]))
                else:
                    error_messages.append(str(value))
            response.data = {"error": " | ".join(error_messages)}
        else:
            # fallback
            response.data = {"error": str(response.data)}

    return response
