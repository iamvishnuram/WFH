import re
from django import template

register = template.Library()

@register.filter(name='clean_username')
def remove_text_after_at(email):
    # Find the position of the "@" symbol
    at_position = email.find('@')
    # Check if the "@" symbol was found
    if at_position != -1:
        # Slice the string to keep only the part before the "@" symbol
        cleaned_email = email[:at_position]
        # Split the cleaned email on uppercase letters to separate first and last names
        parts = re.split(r'([A-Z][a-z]*)', cleaned_email)
        # Filter out empty strings from the split result
        parts = [part.strip() for part in parts if part.strip()]
        # Join the parts with a space
        cleaned_email = ' '.join(parts)
        
        return cleaned_email
    else:
        # If "@" symbol is not found, return the original email
        return email
