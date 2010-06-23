# -*- coding: utf-8 -*-

class ValidationError(Exception):
    """Base validation error."""
  
class MissingValueError(ValidationError):
    """A required field is missing."""
    
class BadFormatError(ValidationError):
    """A field does not match the required format."""