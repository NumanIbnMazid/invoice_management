import random
import string
import time
from django.utils.text import slugify
from urllib.parse import urlparse
from django.db import models
from django.dispatch import receiver
import uuid
# PDF imports
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import pdfkit


def random_string_generator(size=4, chars=string.ascii_lowercase + string.digits):
    """[Generates random string]

    Args:
        size (int, optional): [size of string to generate]. Defaults to 4.
        chars ([str], optional): [characters to use]. Defaults to string.ascii_lowercase+string.digits.

    Returns:
        [str]: [Generated random string]
    """
    return ''.join(random.choice(chars) for _ in range(size))


def random_number_generator(size=4, chars='1234567890'):
    """[Generates random number]

    Args:
        size (int, optional): [size of number to generate]. Defaults to 4.
        chars (str, optional): [numbers to use]. Defaults to '1234567890'.

    Returns:
        [str]: [Generated random number]
    """
    return ''.join(random.choice(chars) for _ in range(size))


def simple_random_string():
    """[Generates simple random string]

    Returns:
        [str]: [Generated random string]
    """
    timestamp_m = time.strftime("%Y")
    timestamp_d = time.strftime("%m")
    timestamp_y = time.strftime("%d")
    timestamp_now = time.strftime("%H%M%S")
    random_str = random_string_generator()
    random_num = random_number_generator()
    bindings = (
        random_str + timestamp_d + random_num + timestamp_now +
        timestamp_y + random_num + timestamp_m
    )
    return bindings


def simple_random_string_with_timestamp(size=None):
    """[Generates random string with timestamp]

    Args:
        size ([int], optional): [Size of string]. Defaults to None.

    Returns:
        [str]: [Generated random string]
    """
    timestamp_m = time.strftime("%Y")
    timestamp_d = time.strftime("%m")
    timestamp_y = time.strftime("%d")
    random_str = random_string_generator()
    random_num = random_number_generator()
    bindings = (
        random_str + timestamp_d + timestamp_m + timestamp_y + random_num
    )
    if not size == None:
        return bindings[0:size]
    return bindings


def unique_slug_generator(instance, field=None, new_slug=None):
    """[Generates unique slug]

    Args:
        instance ([Model Class instance]): [Django Model class object instance].
        field ([Django Model Field], optional): [Django Model Class Field]. Defaults to None.
        new_slug ([str], optional): [passed new slug]. Defaults to None.

    Returns:
        [str]: [Generated unique slug]
    """
    if field == None:
        field = instance.title
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(field[:50])

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def url_check(url):
    """[Checks if a provided string is URL or Not]

    Args:
        url ([str]): [URL String]

    Returns:
        [bool]: [returns True if provided string is URL, otherwise returns False]
    """

    min_attr = ('scheme', 'netloc')

    try:
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            return True
        else:
            return False
    except:
        return False


def autoUniqueIdWithField(fieldname):
    """[Generates auto slug integrating model's field value and UUID]

    Args:
        fieldname ([str]): [Model field name to use to generate slug]
    """

    def decorator(model):
        # some sanity checks first
        assert hasattr(model, fieldname), f"Model has no field {fieldname}"
        assert hasattr(model, "slug"), "Model is missing a slug field"

        @receiver(models.signals.pre_save, sender=model, weak=False)
        def generate_unique_id(sender, instance, *args, raw=False, **kwargs):
            if not raw and not getattr(instance, fieldname):
                source = getattr(instance, fieldname)
                
                def generate():
                    uuid = random_number_generator(size=12)
                    Klass = instance.__class__
                    qs_exists = Klass.objects.filter(uuid=uuid).exists()
                    if qs_exists:
                        generate()
                    else:
                        instance.uuid = uuid
                    pass
                
                # generate uuid
                generate()
                
        return model
    return decorator


def autoslugWithFieldAndUUID(fieldname):
    """[Generates auto slug integrating model's field value and UUID]

    Args:
        fieldname ([str]): [Model field name to use to generate slug]
    """

    def decorator(model):
        # some sanity checks first
        assert hasattr(model, fieldname), f"Model has no field {fieldname}"
        assert hasattr(model, "slug"), "Model is missing a slug field"

        @receiver(models.signals.pre_save, sender=model, weak=False)
        def generate_slug(sender, instance, *args, raw=False, **kwargs):
            if not raw and not instance.slug:
                source = getattr(instance, fieldname)
                try:
                    slug = slugify(source)[:123] + "-" + str(uuid.uuid4())
                    Klass = instance.__class__
                    qs_exists = Klass.objects.filter(slug=slug).exists()
                    if qs_exists:
                        new_slug = "{slug}-{randstr}".format(
                            slug=slug,
                            randstr=random_string_generator(size=4)
                        )
                        instance.slug = new_slug
                    else:
                        instance.slug = slug
                except Exception as e:
                    instance.slug = simple_random_string()
        return model
    return decorator


def autoslugFromField(fieldname):
    """[Generates auto slug from model's field value]

    Args:
        fieldname ([str]): [Model field name to use to generate slug]
    """

    def decorator(model):
        # some sanity checks first
        assert hasattr(model, fieldname), f"Model has no field {fieldname!r}"
        assert hasattr(model, "slug"), "Model is missing a slug field"

        @receiver(models.signals.pre_save, sender=model, weak=False)
        def generate_slug(sender, instance, *args, raw=False, **kwargs):
            if not raw and not instance.slug:
                source = getattr(instance, fieldname)
                try:
                    slug = slugify(source)
                    Klass = instance.__class__
                    qs_exists = Klass.objects.filter(slug=slug).exists()
                    if qs_exists:
                        new_slug = "{slug}-{randstr}".format(
                            slug=slug,
                            randstr=random_string_generator(size=4)
                        )
                        instance.slug = new_slug
                    else:
                        instance.slug = slug
                except Exception as e:
                    instance.slug = simple_random_string()
        return model
    return decorator


def autoslugFromUUID():
    """[Generates auto slug using UUID]
    """

    def decorator(model):
        assert hasattr(model, "slug"), "Model is missing a slug field"

        @receiver(models.signals.pre_save, sender=model, weak=False)
        def generate_slug(sender, instance, *args, raw=False, **kwargs):
            if not raw and not instance.slug:
                try:
                    instance.slug = str(uuid.uuid4())
                except Exception as e:
                    instance.slug = simple_random_string()
        return model
    return decorator


def generate_unique_username_from_email(instance):
    """[Generates unique username from email]

    Args:
        instance ([model class object instance]): [model class object instance]

    Raises:
        ValueError: [If found invalid email]

    Returns:
        [str]: [unique username]
    """

    # get email from instance
    email = instance.email

    if not email:
        raise ValueError("Invalid email!")

    def generate_username(email):
        return email.split("@")[0][:15] + "__" + simple_random_string_with_timestamp(size=5)

    generated_username = generate_username(email=email)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(username=generated_username).exists()

    if qs_exists:
        # recursive call
        generate_unique_username_from_email(instance=instance)

    return generated_username


def render_to_pdf(template_src, context_dict={}):
    """[summary]

    Args:
        template_src ([str]): [path of html file to render]
        context_dict (dict, optional): [additional contexts]. Defaults to {}.

    Returns:
        [HttpResponse/None]: [Django HttpResponse object or None]
    """
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def render_template(template_src, context_dict={}):
    """[summary]

    Args:
        template_src ([str]): [path of html file to render]
        context_dict (dict, optional): [additional contexts]. Defaults to {}.

    Returns:
        [HttpResponse/None]: [Django HttpResponse object or None]
    """
    template = get_template(template_src)
    html = template.render(context_dict)
    return html


def generate_pdf_with_pdfkit(template_src=None, context=None, options=None, css=[], filename="Download.pdf"):
    try:
        if not options:
            options = {
                'page-size': 'Letter',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
                'encoding': "UTF-8",
                'custom-header': [
                    ('Accept-Encoding', 'gzip')
                ],
                'cookie': [
                    ('cookie-empty-value', '""')
                ],
                'no-outline': None
            }
        
        template = render_template(template_src=template_src, context_dict=context)
        
        pdf = pdfkit.from_string(
            template, options=options, css=css
        )
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
        return response
    
    except Exception as E:
        return HttpResponse(str(E), content_type='text/plain')
