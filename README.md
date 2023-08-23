
# WS Queue Manager

This is an open-source Discord bot designed to facilitate WS signups for single corporations.

## Features

- **Feature 1**: WS queue management.
- **Feature 2**: Single corporation support.
- **Feature 3**: Simple and easy to expand on.

## Installation & Setup

### Prerequisites

- Python [Version 3.11]
- A device to run the bot on (e.g., a Raspberry Pi, a VPS, etc.)
- Set up a discord app, then the bot, and ahve the token handy: https://discord.com/developers/docs/getting-started

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/WatsonMLDev/WSDiscordBot.git
   cd WSDiscordBot
   ```

2. **Install the required packages**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the bot**

   ```bash
   python app.py
   ```
## Usage

In Discord, you MUST run the `$config` command to set up the bot. This will link the necessary channels and roles for the bot to function.
After running the `$config` command, you can use the `/help` command to see a list of commands.

## Persistent Databases
When you pull new versions, more than likely your database will be over-written. Make sure to implement some type of database saving plan. 

One method is to fork this repository, add this repo as an upstream dependency to your fork, then implement some type of cloud saving.

Another is to use a syncing application (like Syncthing) to restore the DB on updates.

## How to Contribute

We welcome contributions from everyone. Here's how you can contribute:

1. **Create a new branch**: 

   ```bash
   git checkout -b [branch-name]
   ```

2. **Make your changes** and then commit them:

   ```bash
   git add .
   git commit -m "[brief description of your changes]"
   ```

3. **Push your changes**:

   ```bash
   git push origin [branch-name]
   ```

4. **Create a pull request**: Go to the 'Pull requests' tab of the  repository and click on 'New pull request'. Select the branch you created, then click on 'Create pull request'.

Before creating a pull request, please ensure your code adheres to our coding standards and conventions.
