"""
email_bridge.py

Provides a simple bridge to send mail locally via a Ruby script.
"""

import os
import subprocess

# Path to the Ruby mailer script in the same directory
MAILER = os.path.join(os.path.dirname(__file__), "mailer.rb")


def send_local_mail(question: str, answer: str):
    """
    Send a question and answer pair to the local mailer script as environment variables.

    This uses subprocess.Popen to fire-and-forget without waiting for completion.
    """
    env = os.environ.copy()
    env.update(QUESTION=question, ANSWER=answer)
    # pylint: disable=consider-using-with
    subprocess.Popen(["ruby", MAILER], env=env)
