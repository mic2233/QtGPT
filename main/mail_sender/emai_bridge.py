# email_bridge.py
import os, subprocess, shlex

MAILER = os.path.join(os.path.dirname(__file__), "mailer.rb")

def send_local_mail(question: str, answer: str):
    env = os.environ.copy()
    env.update(QUESTION=question, ANSWER=answer)
    # fire-and-forget; no need to wait
    subprocess.Popen(["ruby", MAILER], env=env)