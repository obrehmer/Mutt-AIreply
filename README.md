# Mutt: Automate Reply Mails with OpenAI

This project enables automatic email replies generated by OpenAI integrated into Mutt. It uses scripts to create the reply and edit it in Mutt before sending.


![AI Generated Reply](https://we.olifani.eu/images/muttai.png)


## Setup

You need an Account on https://platform.openai.com/ and an API Key. Store the key as the env variable 

```
export OPENAI_API_KEY='sk-proj-XXXXXXXXXXXXXXXXXXXXXXXXXX'
```

### 1. Create the necessary files:

#### Checkout the format.py to .mutt/format.py



## Create a wrapper .mutt/email_file

```
#!/usr/bin/env bash

message=$(cat)

echo "${message}" | ~/.mutt/format.py > "/tmp/xxx"

```

## and .mutt/aireply

```
#!/bin/bash
vim $1 "+:call AIReply()"
```

## Make the scripts executable


Ensure all scripts are executable:

```
chmod +x .mutt/format.py  .mutt/email_file .mutt/aireply
```


##  Add the AIReply function to your ~/.vimrc:

Add the following function to your Vim configuration (~/.vimrc):


```
function! AIReply()
  %d_
  r /tmp/xxx
  0d_
  w
endfunction

```
## Add 2 macros to the .muttrc

Macro to create the email template:

```
macro index,pager S "| ~/.mutt/email_file <enter>"
```

Macro for auto-reply with the AI-generated message:

```
macro index,pager A "<enter-command>set editor=~/.mutt/aireply<enter><reply><edit-from><enter><enter><enter>"  "Auto-reply + archive"

```


## Usage

- Open the email you want to reply to.
- Press S to generate the AI reply template. The message will be saved to /tmp/xxx (or another location defined in ~/.mutt/email_file).
- Press A to open the reply in Vim. The AI-generated reply will appear in the editor.
- Simply send the email.
