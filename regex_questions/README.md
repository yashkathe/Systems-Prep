# Regex Questions

## Notes - part 1

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

## Notes - part 2

In regex:

- **.\*** (_greedy_) matches as much as possible before allowing the next part
  of the pattern to continue.
- **.\*?** (**non-greedy or lazy**) matches as little as possible before
  allowing the next part of the pattern to continue.

### Example

**Greedy .\***

Pattern: a.\*b String: axxxbxxxbyyyb Match: axxxbxxxbyyyb (takes the longest
match)

**Non-Greedy .\*?**

Pattern: a.\*?b String: axxxbxxxbyyyb Match: axxxb (takes the shortest match)

So, ._ is greedy, while ._? is non-greedy.

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

### Q3

Parse the file and extract all failed test cases along with their timestamps.
Save the output in a new file called failed_tests.txt with this format:

    TEST_CASE_2: 2025-01-14 10:20:45
    TEST_CASE_3: 2025-01-14 10:22:00
    TEST_CASE_5: 2025-01-14 10:30:00

### Q4

Memory Failure Analysis

Extract failure bits:

    2025-01-14 10:15:30 ERROR Memory bit 1010 stuck at 1
    2025-01-14 10:20:00 INFO System running normally
    2025-01-14 10:25:45 ERROR Memory bit 1100 stuck at 0
    2025-01-14 10:30:30 ERROR Memory bit 1010 stuck at 1
    2025-01-14 10:40:00 INFO System rebooted
    2025-01-14 10:50:15 ERROR Memory bit 1110 stuck at 1

### Q5

Parse the log file and categorize the results into PASS and FAIL. Save the
results into two separate files, pass_logs.txt and fail_logs.txt.

data log:

    TEST_CASE_1,PASS
    TEST_CASE_2,FAIL
    TEST_CASE_3,PASS
    TEST_CASE_4,FAIL
    TEST_CASE_5,FAIL
