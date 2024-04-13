# Import necessary libraries from uagents package
from uagents import Agent, Context, Model
from pydantic import BaseModel
from typing import Dict, Any

# Define the user agent with specific configuration details
user_agent = Agent(
    name="user_agent",
    seed="user secret phrase",  # Set a secret phrase for the user agent
    port=8009,  # Port number
    endpoint=["http://localhost:8009/submit"],
)


# Define a custom message class for the user's input
class UserInput(Model):
  amount: float
  risk: float


# Event handler for the user agent's startup event
@user_agent.on_event("startup")
async def handle_startup(ctx: Context) -> None:
  """Handles the startup event by prompting the user for input and sending it to the next agent."""
  ctx.logger.info("User Agent started.")

  # Prompt the user for the amount they are willing to invest
  amount_to_invest = float(
      input("Enter the amount you are willing to invest: "))
  risk_level_percentage = float(
      input("Enter your risk level as a percentage (e.g., 10 for 10%): "))
  risk_level_decimal = risk_level_percentage / 100

  # Create a UserInput object with the user's input
  user_input = UserInput(amount=amount_to_invest, risk=risk_level_decimal)
  ctx.logger.info(
      f"User input - Amount to invest: {amount_to_invest}, Risk level: {risk_level_decimal}"
  )

  # Send the UserInput message to the next agent
  # Replace with the actual address of the next agent
  await ctx.send("agent1qtc63cluyqxyvu3zmugesmuawl4eq3jzzu2euygszn4fzd5altqjsjkrjpy", user_input)


if __name__ == "__main__":
  user_agent.run()
