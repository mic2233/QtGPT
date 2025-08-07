#!/usr/bin/env ruby
# local_mailer.rb  – expects QUESTION, ANSWER, SMTP_HOST, SMTP_PORT in ENV
require "mail"

smtp_host = ENV.fetch("SMTP_HOST", "localhost")
smtp_port = Integer(ENV.fetch("SMTP_PORT", 1025))

Mail.defaults do
  delivery_method :smtp,
    address: smtp_host,
    port:    smtp_port
end

question = ENV["QUESTION"] || "(none)"
answer   = ENV["ANSWER"]   || "(none)"

Mail.deliver do
  from    "chatbot@local.test"
  to      "inbox@local.test"
  subject "Chat transcript"
  body    "Q: #{question}\n\nA: #{answer}"
end
