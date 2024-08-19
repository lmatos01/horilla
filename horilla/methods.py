import contextlib

from django.contrib.contenttypes.models import ContentType


def get_horilla_model_class(app_label, model):
    """
    Retrieves the model class for the given app label and model name using Django's ContentType framework.

    Args:
        app_label (str): The label of the application where the model is defined.
        model (str): The name of the model to retrieve.

    Returns:
        Model: The Django model class corresponding to the specified app label and model name.

    """
    content_type = ContentType.objects.get(app_label=app_label, model=model)
    model_class = content_type.model_class()
    return model_class


def dynamic_attr(obj, attribute_path):
    """
    Retrieves the value of a nested attribute from a related object dynamically.

    Args:
        obj: The base object from which to start accessing attributes.
        attribute_path (str): The path of the nested attribute to retrieve, using
        double underscores ('__') to indicate relationship traversal.

    Returns:
        The value of the nested attribute if it exists, or None if it doesn't exist.
    """
    attributes = attribute_path.split("__")

    for attr in attributes:
        with contextlib.suppress(Exception):
            Contract = get_horilla_model_class(app_label="payroll", model="contract")
            if isinstance(obj.first(), Contract):
                obj = obj.filter(is_active=True).first()

        obj = getattr(obj, attr, None)
        if obj is None:
            break
    return obj
