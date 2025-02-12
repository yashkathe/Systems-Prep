# **Practice File (`sed_practice.txt`)**

```plaintext
# This is a sample file for practicing sed commands
Line 1: Hello, this is a test.
Line 2: The quick brown fox jumps over the lazy dog.
Line 3: My email is user@example.com.
Line 4: Replace 123-456-7890 with a new phone number.
Line 5: This is line number five.
Line 6: The password is secret123.
Line 7: The cost of the item is $99.99.
Line 8: Dates: 2023-01-01, 2024/02/02, 01.03.2025
Line 9: Remove this line entirely.
Line 10: "Quoted text should be modified."
Line 11: THIS LINE IS IN UPPERCASE.
Line 12: this line is in lowercase.
Line 13:    There are leading spaces here.
Line 14: There are trailing spaces here.
Line 15: Duplicate word word should be removed.
Line 16: User: admin, Password: pass123, Role: superuser.
Line 17: <html><body>This is inside HTML tags.</body></html>
Line 18: 192.168.1.1 is a private IP address.
Line 19: The item costs ₹500 in India and $10 in the US.
Line 20: END OF FILE
```

---

## **1. Substituting text**

- Replace **"test"** with **"example"**:

  ```bash
  sed 's/test/example/' sed_practice.txt
  ```

- Replace all occurrences of **"line"** with **"row"** (case insensitive):

  ```bash
  sed 's/line/row/gi' sed_practice.txt
  ```

## **2. Deleting lines**

- Remove **line 9** entirely:

  ```bash
  sed '9d' sed_practice.txt
  ```

- Remove all lines containing **"password"**:

  ```bash
  sed '/password/d' sed_practice.txt
  ```

## **3. Inserting and Appending lines**

- Insert **"---- HEADER ----"** before the first line:

  ```bash
  sed '1i ---- HEADER ----' sed_practice.txt
  ```

- Append **"---- FOOTER ----"** after the last line:

  ```bash
  sed '$a ---- FOOTER ----' sed_practice.txt
  ```

## **4. Removing spaces**

- Remove leading spaces:

  ```bash
  sed 's/^ *//' sed_practice.txt
  ```

- Remove trailing spaces:

  ```bash
  sed 's/ *$//' sed_practice.txt
  ```

## **5. Working with numbers**

- Replace all **digits** with `X`:

  ```bash
  sed 's/[0-9]/X/g' sed_practice.txt
  ```

- Remove lines containing **prices (₹, $)**:

  ```bash
  sed '/[$₹]/d' sed_practice.txt
  ```

## **6. Removing duplicate words**

- Remove consecutive duplicate words:

  ```bash
  sed 's/\b\(\w\+\) \1\b/\1/' sed_practice.txt
  ```

## **7. Extracting Email & IP addresses**

- Extract only email addresses:

  ```bash
  sed -n 's/.*\([a-zA-Z0-9._%+-]\+@[a-zA-Z0-9.-]\+\.[a-zA-Z]\+\).*/\1/p' sed_practice.txt
  ```

- Extract IP addresses:

  ```bash
  sed -n 's/.*\([0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\).*/\1/p' sed_practice.txt
  ```
