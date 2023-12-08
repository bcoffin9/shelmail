# Gmail SMTP Send through Shell: ShelMail

## Inspired by Computer Networking: A Top-Down Approach 8th Edition

```
:'######::'##::::'##:'########:'##:::::::'##::::'##::::'###::::'####:'##:::::::
'##... ##: ##:::: ##: ##.....:: ##::::::: ###::'###:::'## ##:::. ##:: ##:::::::
 ##:::..:: ##:::: ##: ##::::::: ##::::::: ####'####::'##:. ##::: ##:: ##:::::::
. ######:: #########: ######::: ##::::::: ## ### ##:'##:::. ##:: ##:: ##:::::::
:..... ##: ##.... ##: ##...:::: ##::::::: ##. #: ##: #########:: ##:: ##:::::::
'##::: ##: ##:::: ##: ##::::::: ##::::::: ##:.:: ##: ##.... ##:: ##:: ##:::::::
. ######:: ##:::: ##: ########: ########: ##:::: ##: ##:::: ##:'####: ########:
:......:::..:::::..::........::........::..:::::..::..:::::..::....::........::
```

---

## How to use

- If using MacOS, ensure you have run the Install Certificates.command file in your Python Application folder.
- Use the following link to add an App Password to your Google Mail account:
  - https://support.google.com/mail/answer/185833?hl=en#zippy=
  - Note down the password
- run `python3 src/mail_server.py`
- Follow the prompts, using your gmail address, app password, and recipient address you want to send to
- After using the program, it's recommended by Google to delete your app password

---

## Passing Criteria

1. A secure connection is used to communicate with Google's SMTP mail server
2. No external library is used, i.e. `smtplib.py`
3. User can send a simple message to one recipient through their email

---

## Future ideas

- Test framework
