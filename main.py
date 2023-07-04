import alerter
import emailsender
import pandas as pd

from time import sleep


def main(interval):  # interval is in hours
    df = pd.read_csv("users.csv")

    while True:
        names = df.Name

        emails = df.Email

        for i in range(len(emails)):

            try:
                email = emails[i]
                name = names[i]

                print(f"-->\tEMAIL SENT TO: {str(name)} at {str(email)}\t", flush=True)

                emailsender.sendEmail(
                    email=email,
                    name=name,
                    alerts=alerter.textualize(alerter.formData(email=email))
                )  # these are just the variables i use for my courier email template

                print("\n", flush=True)

            except IndexError:
                pass

        sleep(interval * 3600)  # converts interval to seconds --> waits n seconds to scan again


main(interval=24)
