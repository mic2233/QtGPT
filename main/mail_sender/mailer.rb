#!/usr/bin/env ruby
# local_mailer.rb  – expects QUESTION and ANSWER in the environment
require "mail"

Mail.defaults do
  delivery_method :smtp, address: "localhost", port: 1025   # MailHog/MailCatcher
end

question = ENV["QUESTION"] || "(none)"
answer   = ENV["ANSWER"]   || "(none)"

Mail.deliver do
  from    "chatbot@local.test"
  to      "inbox@local.test"         # any address, MailHog just stores it
  subject "Chat transcript"
  body    "Q: #{question}\n\nA: #{answer}"
end
