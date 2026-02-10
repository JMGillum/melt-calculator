# Style Guideline

This document will serve as the style guideline for the precious metals calculator project, including the coin-data repository. The tree and treasure submodules of this project are considered separate projects, and these style guidelines will not apply to them (although they may coincidentally follow these guidelines). The purpose of these guidelines are to improve code readability and comprehension. Consistent naming conventions aid in decoding what kind of object the name belongs to (ex: variable or class), as well as makes the code easier to parse through. Because of this, all code committed should follow the guidelines set forth in this document.

## Definitions

Although some of the terms used here may have multiple meanings, the important ones will be defined below to avoid ambiguitiy. The definiton here may not coincide with the most prevalant meaning of the term, but the definition here will be the one used when the term is used within this document.  

### Naming

* Name: the string of characters used to reference objects, whether these objects are variables, classes, modules, etc. Ex: x=5. "x" would be the name for this variable.
* Camel Case: A naming convention in which multiple words are combined without any space character. The first letter of each word after the first is capitalized and every other character is lowercase.
* Pascal Case: A naming convention that is exactly the same as camel case, except that the first letter of the first word is also capitalized.
* Snake Case: A naming convention where multiple words are combined with an underscore '_' as the space characters. All letters in the name are lowercase.

**name = fetch report**  
Camel case: fetchReport  
Pascal case: FetchReport  
Snake case: fetch_report  

## Naming conventions

The following rules will apply to the names of object. 
1. Variable names are to always start with a letter. The exception to this are for anything that is builtin to the Python language, such as "__main__". The purpose of this rule is to avoid naming conflicts and to imrpove recognition.
2. Variable names should always be in snake case. There is no specific reason for snake case, however consistency will improve readability.
3. Function names should always be in Pascal case.
4. Class names should always be in Pascal case.
5. File names should always be in camel case.

## Quotes

1. Double-quotes should be used wherever possible. Single-quotes should only be used when necessary, such as for quoting things within double-quoted strings. See the examples below:  

```python
# Double quotes should be used as much as possible, even if they have to be escaped within a string
prompt_string = "Enter a prompt:"
x = some_dict["some_key"]
print("\"This is a quote\"")

# Here is when single quotes should be used.
print(f"The value of x: {some_dict['some_key']}")
# Although, this could be rewritten to store x as a variable before printing, 
# in order to remove the dependency on single quotes. However, this is acceptable usage.
```

## Spacing

1. Indentations should be multiples of four spaces "    ", the tab "\t" character should never be used. The only exception is when the tab character is required, such as within makefiles.
2. The following arithmetic operators should have spacing beside them: + - * / += -= *= /= . Negation (-a), increment (++a or a++), and decrement (--a or a--) operators should be touching the variable they apply to.
3. Two empty lines should be placed before any function definition, as well as before global code between or after function definitions.
4. A newline should be at the end of every file.
5. All comments that describe something below them, should have one empty line above them. See below:

```python
# Incorrect

# The quadratic equation (-b +- sqrt(b^2 - 4ac))/2a
a = 1
b = 5
c = 10
# The squareroot portion 
result = math.sqrt(b*b-4*a*c)
# The plus or minus portion as well as final division
result_plus = (-b + result) / (2 * a)
result_minus = (-b - result) / (2 * a)


# Correct

# The quadratic equation (-b +- sqrt(b^2 - 4ac))/2a
a = 1
b = 5
c = 10

# The squareroot portion 
result = math.sqrt(b*b-4*a*c)

# The plus or minus portion as well as final division
result_plus = (-b + result) / (2 * a)
result_minus = (-b - result) / (2 * a)
```

## Functions

1. Functions should be broken down into the smallest functional piece possible. It is more desirable to have multiple small functions than one large function. This aids code reuse and can imrpove readability.
2. Type hints should be used for each parameter that expects only one or two different datatypes. The same applies for return values.

## Comments

1. There should only be multiline comment characters when the comment spans more than 5 lines. See the example below:

```python
"""
This is a comment enclosed within multiple lines.
It violates the style guidelines because it uses the multiline comment characters and is only 4 lines long.
(three double-quotes)
"""

# This is a comment that spans multiple lines,
# but it is comprised of multiple single line comments.
# This is the correct way to do this.
```

2. Comments should be placed on the line(s) above any control logic that explains what causes the code to enter these blocks. It should be placed above the statement, not below, or to the side of it. See below:

```python
# Suppose that x stores the number of files that matched a pattern.

# This comment here describes what is significant about 
# the control block below and in what situations that control 
# flow will enter it. Notice that this comment is above the if statement
if x > 3:
    print("There are too many files here. Please delete them")

# This comment describes what is significant about control 
# flow entering the else block below. Notice how there is a 
# empty line between the code above and this comment.
else:
    print("Everything is fine.")

```

3. All files should contain a header comment that generally describes the contents of the file. It may also optionally have the author of the file and the date of last modification.
4. All function should include a comment below the function definition line. This comment should include a description of what the function does (not how its implemented, just what it does). Below that should be each parameter with a description of the parameter, what it is for, and what kind(s) of datatype it should be. Finally, there should be a line stating what the function returns.

```python
def foo(x:int|float,y:int|float)->int|float:
    """ Returns the square of the product of the two variables.

    Args:
        x (int|float): The first value for the arithmetic operation
        y (int|float): The first value for the arithmetic operation

    Returns (int|float): The square of the product of the two variables
    """
    return x * x * y *y
```
