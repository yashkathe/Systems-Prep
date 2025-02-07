# Regex Questions

## Notes

(?:) - non capturing group

. - Any Character Except New Line  
\d - Digit (0-9)  
\D - Not a Digit (0-9)  
\w - Word Character (a-z, A-Z, 0-9, \_)  
\W - Not a Word Character  
\s - Whitespace (space, tab, newline)  
\S - Not Whitespace (space, tab, newline)

\b - Word Boundary  
\B - Not a Word Boundary  
^ - Beginning of a String  
$ - End of a String

[] - Matches Characters in brackets  
[^ ] - Matches Characters NOT in brackets  
| - Either Or  
( ) - Group

Quantifiers:  
\* - 0 or More  
\+ - 1 or More  
? - 0 or One  
{3} - Exact Number  
{3,4} - Range of Numbers (Minimum, Maximum)

### Questions

### Q1

Dummy Data:

apple 123 banana cat_dog 4567 elephant hello_world 89 regex_test 1011
fun_with_regex 1213 ABCD_efgh 1415

Question 1:

    Write a regex pattern to match all words that contain an underscore (_).

Question 2:

    Write a regex pattern to match all numbers that have exactly 4 digits.

### Q2

Question 1:

Write a regex pattern to match all valid email addresses from the text. A valid
email:

    Must have an "@" symbol.
    Should have a domain name followed by a top-level domain (e.g., .com, .net, .io).

Question 2:

Write a regex pattern to match valid IPv4 addresses from the text. A valid IPv4:

    Consists of four groups of numbers (0-255) separated by dots (.).
    Each group should be between 0 and 255.
    The invalid IP (999.999.999.999) should not match.
