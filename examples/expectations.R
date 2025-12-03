# Probability predictions
#
# example file of a simple experiment with llms
# check out "setup.R" before for basic usage of ellmer package
# you need to have set your API_KEY before this runs

library(ellmer)

# Define inputs --------------------------

# define model
model <- "openai/gpt-oss-120b"

# define events to predict
events <- c(
  "Trump will be president in 2028",
  "Global average temperature will increase by more than 1.5°C by 2030",
  "AI will pass the Turing test by 2027",
  "Bitcoin price will exceed $100,000 by end of 2026",
  "Humans will land on Mars by 2035"
)

# number of repetitions
n <- 3

# Define response structure --------------------------

# define response types for llm
response_type <- type_object(
  min_prob = type_number("Minimum probability (use same as prob if point estimate)"),
  prob = type_number("Point probability estimate"),
  max_prob = type_number("Maximum probability (use same as prob if point estimate)")
)

# Run experiment --------------------------

# initialize variables
results_list <- list()
counter <- 1

cat("Sending", length(events) * n, "prompts to the LLM...\n")

# loop over all events and all n repetitions
for (i in seq_along(events)) {
  for (j in 1:n) {
    chat <- chat_openrouter(
      model = model,
      system_prompt = paste(
        "You are an expert forecaster providing probability estimates.",
        "Reply with only the requested JSON structure and nothing else."
      )
    )

    # define prompt
    prompt <- sprintf(
      paste(
        "What is the probability that: %s?",
        "Provide your answer as a percentage between 0 and 100.",
        "If uncertain, you may provide an interval by its minimal and maximal probability."
      ),
      events[i]
    )

    # save result
    result <- chat$chat_structured(prompt, type = response_type)

    # store each run in one list entry
    results_list[[counter]] <- data.frame(
      event = events[i],
      run = j,
      minp = result$min_prob,
      p = result$prob,
      maxp = result$max_prob
    )

    counter <- counter + 1
  }
}

cat("Experiment complete.\n")

# Combine results --------------------------

# extract results from list into data.frame
final_predictions <- do.call(rbind, results_list) |>
  # generate additional variables
  transform(
    interval_width = maxp - minp,
    is_interval = minp != maxp
  )

# Display results --------------------------

print(final_predictions)

# Plot results --------------------------

library(ggplot2)

final_predictions |>
  transform(event = factor(event, levels = rev(unique(event)))) |>
  ggplot(aes(y = event, group = run)) +
  geom_errorbar(aes(xmin = minp, xmax = maxp),orientation = "y",
                 width = 0.3, position = position_dodge(width = 0.5)) +
  geom_point(aes(x = p), size = 3, position = position_dodge(width = 0.5)) +
  labs(
    x = "Probability (%)",
    y = NULL,
    title = "LLM Probability Predictions with Uncertainty Intervals"
  ) +
  theme_minimal()
