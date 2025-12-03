# run once
# install.packages("ellmer")

library(ellmer)

# # get your openrouter api key first, then set it with
# Sys.setenv(OPENROUTER_API_KEY = "YOUR_API_KEY")
# # check with
# Sys.getenv("OPENROUTER_API_KEY")

# create chat instance
chat <- chat_openrouter(
  model = "mistralai/mixtral-8x7b-instruct",
  system_prompt = "You are a helpful and creative assistant."
)

# start a conversation
response <- chat$chat("Who is talking to me?",echo = F)

# print the response
print(response)

