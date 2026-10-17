class OutOfSampleError(Exception):

    # OutOfSampleError --> Name of custom exception 
    # Exception is the built in exception class that my custom class inherits from 


    
    """
    Raised when a new input contains feature values
    outside the historical min/max range.
    """
    pass 


# Feature4 with value 1.0 is outside historical range [0.1, 0.9]
